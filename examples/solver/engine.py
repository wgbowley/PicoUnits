"""
Filename: engine.py
Author: William Bowley

Description:
    Transient thermal solver for the 2D heat equation PDE
    using picounits to show unit-boundary abstractions.
    
    NOTE:
    This is a demonstration model and is not intended to 
    match a refined finite element solver
"""

import numpy as np

from shapely import box, MultiPoint
from shapely.ops import triangulate

from picounits import UnitError, Q, strip_quantity
from picounits.extensions.loader import DynamicLoader

from picounits.constants import (
    LENGTH, TEMPERATURE, TIME, VOLUMETRIC_HEATING,
    VOLUMETRIC_HEAT_CAPACITY, THERMAL_CONDUCTIVITY
)


class PreProcessor:
    """ Builds geometry and then meshes the problem domain """
    @staticmethod
    def rectangle(bottom_left: tuple[Q, Q], length: Q, height: Q) -> list:
        """ Creates a square vector geometry """
        x, y = bottom_left

        for item in (x, y, length, height):
            if isinstance(item, Q):
                if item.unit == LENGTH:
                    break

            msg = f"{item!r} must be have unit {LENGTH} not {item.unit!r}"
            raise UnitError(msg)

        return [x.value, y.value, (x + length).value, (y + height).value]

    def __init__(self, domain: list, source: list, density: int = 20) -> None:
        """ Constructs mesh based on geometry built via static methods """
        # Saves raw coordinates
        self.domain_coordinates = domain

        # Converts source to shapely box
        source = box(source[0], source[1], source[2], source[3])
        self.source_box_coords = list(source.exterior.coords)

        # Builds grid around geometry
        bx, by, tx, ty = domain
        x_coords, y_coords = np.linspace(bx, tx, density), np.linspace(by, ty, density)
        points = MultiPoint([(x, y) for x in x_coords for y in y_coords])

        # Meshes the geometry
        all_points_list = [(p.x, p.y) for p in points.geoms] + self.source_box_coords
        refined_points = MultiPoint(all_points_list)

        # Saves mesh
        self.mesh = triangulate(refined_points)
        self.source_box = source


class Solver:
    """ Solves the transient thermal PDE over 2D geometry using FEM """
    def __init__(self, preprocessor: PreProcessor) -> None:
        """ Initializes the solver """
        # Saves mesh and raw geometry for matrix assembly
        self.mesh = preprocessor.mesh
        self.domain = preprocessor.domain_coordinates
        self.source = preprocessor.source_box

        # Calculates the number of nodes and elements
        nodes = []
        for triangle in self.mesh:
            nodes.extend(list(triangle.exterior.coords))

        self.unique_nodes = np.unique(nodes, axis=0)
        self.num_nodes = len(self.unique_nodes)

        self.num_element = len(self.mesh)

        # Configures the conductivity array, load vector, mass and stiffness matrix
        self.connectivity = []
        self.load_vector = np.zeros(self.num_nodes)
        self.m_stiffness = np.zeros((self.num_nodes, self.num_nodes))
        self.m_mass = np.zeros((self.num_nodes, self.num_nodes))

        # Post init variables
        self.source_material = None
        self.domain_material = None

        self.time_step = 0
        self.axial_length = 0
        self.boundary_temp = 0
        self.heating = 0

        self.system = None
        self.connectivity = None
        self.boundary_indices: np.ndarray = None

    def build(self, params: DynamicLoader) -> None:
        """ Builds the simulation domain via assembly of stiffness and mass matrixes """
        # Extracts materials properties
        self.domain_material = params.air
        self.source_material = params.copper

        # Extracts and strips away units after validation
        self.time_step = strip_quantity(params.problem.time_step, TIME)
        self.axial_length = strip_quantity(params.problem.axial_length, LENGTH)
        self.boundary_temp = strip_quantity(params.problem.temperature, TEMPERATURE)
        self.heating = strip_quantity(params.source.power_density, VOLUMETRIC_HEATING)

        self._matrix_assembly()

    def solve(
        self,
        current_solution: np.ndarray | None = None,
        max_iterations: int = 1000,
        tolerance: float = 1e-9,
        penalty: float = 1e12
    ) -> np.ndarray:
        """" Solves the thermal problem for the current time step """
        # Configures the boundary conditions
        x_min, y_min, x_max, y_max = self.domain

        # Creates the boundary indices using tolerance on first iteration
        if self.boundary_indices is None:
            unique_nodes = self.unique_nodes
            self.boundary_indices = np.where(
                (np.abs(unique_nodes[:, 0] - x_min) < tolerance) |
                (np.abs(unique_nodes[:, 0] - x_max) < tolerance) |
                (np.abs(unique_nodes[:, 1] - y_min) < tolerance) |
                (np.abs(unique_nodes[:, 1] - y_max) < tolerance)
            )[0]

        if current_solution is None:
            u_old = np.full(self.num_nodes, self.boundary_temp)
        else:
            u_old = current_solution

        u_crr = u_old.copy()
        for _ in range(max_iterations):
            self.m_stiffness.fill(0)
            self.m_mass.fill(0)
            self.load_vector.fill(0)
            self._matrix_assembly(u_crr)

            # Form the backwards euler equation
            self.system = self.m_mass + self.time_step * self.m_stiffness
            b_rhs = self.m_mass @ u_old + self.time_step * self.load_vector

            # Apply boundary conditions via penalty
            for index in self.boundary_indices:
                self.system[index, index] += penalty
                b_rhs[index] += penalty * self.boundary_temp

            u_next = self._gradient_solver(self.system, b_rhs, u_crr, tolerance)

            if np.linalg.norm(u_next - u_crr) < tolerance:
                return u_next

        return u_next

    def _matrix_assembly(self, current_solution: np.ndarray | None = None) -> None:
        """ Constructs the conductivity array, stiffness and mass matrix"""
        conductivity_map = []
        for index, triangle in enumerate(self.mesh):
            triangle_coordinates = np.array(triangle.exterior.coords)[:3]

            # Only solves the conductivity if is none
            if self.connectivity is None:
                # # Map triangle nodes to their indices within the unique nodes
                indices = []
                for point in triangle_coordinates:
                    # Finds the nodal place via minimal distance across the array
                    distance = np.linalg.norm(self.unique_nodes - point, axis=1)
                    indices.append(np.argmin(distance))
                conductivity_map.append(indices)
            else:
                indices = self.connectivity[index]

            # Calculates basis and triangle area
            axial = self.axial_length
            b, c, area = self._calculate_triangle(triangle_coordinates)

            # Adds heat source to local vector
            temp_dependence = self.domain_material.temp_dependence
            heat_capacity = self.domain_material.volumetric_heat_capacity
            if triangle.intersects(self.source):
                # Updates thermal conductivity and heat capacity
                temp_dependence = self.source_material.temp_dependence
                heat_capacity = self.source_material.volumetric_heat_capacity

                heat_per_node = self.heating * self.axial_length * area / 3
                for i in indices:
                    self.load_vector[i] += heat_per_node

            # Finds local conductivity from current_solution
            if current_solution is not None:
                temp_average = np.mean(current_solution[indices]) * TEMPERATURE
                conductivity = self._interpolate(temp_dependence, temp_average)
            else:
                boundary = self.boundary_temp * TEMPERATURE
                conductivity = self._interpolate(temp_dependence, boundary)

            # Extracts values
            conductivity = strip_quantity(conductivity, THERMAL_CONDUCTIVITY)
            heat_capacity = strip_quantity(heat_capacity, VOLUMETRIC_HEAT_CAPACITY)

            # Calculates local stiffness & local mass [3, 3] matrixes
            local_b = np.array([b, c]) / (2 * area)
            ke_local = conductivity * axial * area * np.dot(local_b.T, local_b)

            a, b, c = [2, 1, 1], [1, 2, 1], [1, 1, 2]
            me_local = heat_capacity * axial * (area / 12) * np.array([a, b, c])

            for i in range(3):
                for j in range(3):
                    self.m_stiffness[indices[i], indices[j]] += ke_local[i, j]
                    self.m_mass[indices[i], indices[j]] += me_local[i, j]

        if self.connectivity is None:
            self.connectivity = np.array(conductivity_map)

    def _calculate_triangle(self, coords: np.ndarray) -> tuple[list, list, float]:
        """ Calculates piecewise linear basis and triangle area via Shoelace Formula """
        # Breaks nodes into coordinates
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        x3, y3 = coords[2]

        # Uses coordinates to calculate (b,c) matrix and area
        b = [y2-y3, y3-y1, y1-y2]
        c = [x3-x2, x1-x3, x2-x1]
        area = 0.5 * abs(x1*b[0] + x2*b[1] + x3*b[2])

        return b, c, area

    def _interpolate(self, points: Q, value: Q) -> Q:
        """ Linear interpolates a quantity list from a specific linked value """
        if value <= points[0][0]:
            return points[0][1]
        if value >= points[-1][0]:
            return points[-1][1]

        for index in range(len(points) - 1):
            x0, x1 = points[index][0], points[index + 1][0]
            y0, y1 = points[index][1], points[index + 1][1]

            if x0 <= value <= x1:
                return y0 + (y1 - y0) / (x1 - x0) * (value - x0)

    def _gradient_solver(
        self,
        A: np.ndarray,
        B: np.ndarray,
        sol: np.ndarray | None = None,
        tolerance: float = 1e-9,
        max_iter: int =1000
    ) -> np.ndarray:
        """ Solvers Ax=b via conjugate gradient solver for Ax=B linear system """
        # Uses old solution as initial guess or empty B matrix
        sol = sol if sol is not None else np.zeros_like(B)

        # Distance A.sol is from B
        distance = B - np.dot(A, sol)
        direction = distance.copy()
        magnitude = np.dot(distance, distance)

        for _ in range(max_iter):
            # Calculates the step size (alpha)
            A_d = np.dot(A, direction)
            alpha = magnitude / np.dot(direction, A_d)

            # Update solution via moving solution by alpha along direction
            sol += alpha * direction
            distance -= alpha * A_d

            # Check magnitude is less than tolerance
            new_magnitude = np.dot(distance, distance)
            if np.sqrt(new_magnitude) < tolerance:
                break

            # Updates search direction and magnitude
            direction = distance + (new_magnitude / magnitude) * direction
            magnitude = new_magnitude

        return sol
