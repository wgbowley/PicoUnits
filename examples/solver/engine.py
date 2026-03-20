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
    VOLUMETRIC_HEAT_CAPACITY, THERMAL_CONDUCTIVITY,
    CONVECTION_COEFFICIENT, DIMENSIONLESS
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

    def __init__(self, domain: list, source: list, density: int = 30) -> None:
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
        self.constructed = False
        self.source_capacity = None
        self.convection = None
        self.source_dependence = None

        self.domain_capacity = None
        self.domain_dependence = None

        self.time_step = 0
        self.axial_length = 0
        self.boundary_temp = 0
        self.heating = 0
        self.tolerance = 0

        self.system = None
        self.connectivity = None
        self.boundary_edges = None
        self.interface_edges = None
        self.boundary_indices: np.ndarray = None

    def build(self, params: DynamicLoader) -> None:
        """ Builds the simulation domain via assembly of stiffness and mass matrixes """
        # Extracts materials properties
        def _decompile(material: DynamicLoader) -> tuple[list, float]:
            """ Validates and decompile's dependence table """
            temp, k_vals = [], []
            for group in material.temp_dependence:
                temperature = strip_quantity(group[0], TEMPERATURE)
                conductivity = strip_quantity(group[1], THERMAL_CONDUCTIVITY)

                temp.append(temperature)
                k_vals.append(conductivity)

            capacity = material.volumetric_heat_capacity
            capacity = strip_quantity(capacity, VOLUMETRIC_HEAT_CAPACITY)
            return (temp, k_vals), capacity

        # Decompile's materials
        self.source_dependence, self.source_capacity = _decompile(params.copper)
        self.domain_dependence, self.domain_capacity = _decompile(params.air)
        convection = params.problem.convection

        # Extracts and strips away units after validation
        self.time_step = strip_quantity(params.problem.time_step, TIME)
        self.axial_length = strip_quantity(params.problem.axial_length, LENGTH)
        self.convection = strip_quantity(convection, CONVECTION_COEFFICIENT)
        self.boundary_temp = strip_quantity(params.problem.temperature, TEMPERATURE)
        self.heating = strip_quantity(params.source.power_density, VOLUMETRIC_HEATING)
        self.tolerance = strip_quantity(params.problem.tolerance, DIMENSIONLESS)

        self._matrix_assembly()

    def solve(
        self,
        current_solution: np.ndarray | None = None,
        max_iterations: int = 1000,
    ) -> np.ndarray:
        """" Solves the thermal problem for the current time step """
        # Configures the boundary conditions
        x_min, y_min, x_max, y_max = self.domain

        # Creates the boundary indices using tolerance on first iteration
        if self.boundary_indices is None:
            unique_nodes = self.unique_nodes
            self.boundary_indices = np.where(
                (np.abs(unique_nodes[:, 0] - x_min) < self.tolerance) |
                (np.abs(unique_nodes[:, 0] - x_max) < self.tolerance) |
                (np.abs(unique_nodes[:, 1] - y_min) < self.tolerance) |
                (np.abs(unique_nodes[:, 1] - y_max) < self.tolerance)
            )[0]

        if current_solution is None:
            u_old = np.full(self.num_nodes, self.boundary_temp)
        else:
            u_old = current_solution

        u_crr = u_old.copy()
        for _ in range(max_iterations):
            self.m_stiffness.fill(0)
            self.load_vector.fill(0)
            self._matrix_assembly(u_crr)

            # Form the backwards euler equation
            self.system = self.m_mass + self.time_step * self.m_stiffness
            b_rhs = self.m_mass @ u_old + self.time_step * self.load_vector

            u_next = self._gradient_solver(self.system, b_rhs, u_crr, self.tolerance)

            if np.linalg.norm(u_next - u_crr) < self.tolerance:
                return u_next

        return u_next

    def _matrix_assembly(self, current_solution: np.ndarray | None = None) -> None:
        """ Constructs the conductivity array, stiffness and mass matrix """
        if not self.constructed:
            conductivity_map = []
            self.boundary_edges = []
            self.interface_edges = []
            x_min, y_min, x_max, y_max = self.domain
            s_xmin, s_ymin, s_xmax, s_ymax = self.source.bounds
            tol = self.tolerance

        for index, triangle in enumerate(self.mesh):
            triangle_coordinates = np.array(triangle.exterior.coords)[:3]

            # --- PRE-PROCESSING MESH DATA (Run once) ---
            if not self.constructed:
                indices = []
                for point in triangle_coordinates:
                    # Map triangle nodes to unique nodes
                    distance = np.linalg.norm(self.unique_nodes - point, axis=1)
                    indices.append(np.argmin(distance))
                conductivity_map.append(indices)

                # Identify Edges for Convection
                for i, j in [(0, 1), (1, 2), (2, 0)]:
                    p1, p2 = triangle_coordinates[i], triangle_coordinates[j]
                    edge_len = np.linalg.norm(p1 - p2)

                    # 1. Domain Boundary Edges
                    on_boundary = (
                        (np.abs(p1[0] - x_min) < tol and np.abs(p2[0] - x_min) < tol) or
                        (np.abs(p1[0] - x_max) < tol and np.abs(p2[0] - x_max) < tol) or
                        (np.abs(p1[1] - y_min) < tol and np.abs(p2[1] - y_min) < tol) or
                        (np.abs(p1[1] - y_max) < tol and np.abs(p2[1] - y_max) < tol)
                    )
                    if on_boundary:
                        self.boundary_edges.append(([indices[i], indices[j]], edge_len))

                    # 2. Source Interface Edges (Where copper meets air)
                    on_source = (
                        (np.abs(p1[0] - s_xmin) < tol and np.abs(p2[0] - s_xmin) < tol 
                         and s_ymin-tol <= p1[1] <= s_ymax+tol) or
                        (np.abs(p1[0] - s_xmax) < tol and np.abs(p2[0] - s_xmax) < tol 
                         and s_ymin-tol <= p1[1] <= s_ymax+tol) or
                        (np.abs(p1[1] - s_ymin) < tol and np.abs(p2[1] - s_ymin) < tol 
                         and s_xmin-tol <= p1[0] <= s_xmax+tol) or
                        (np.abs(p1[1] - s_ymax) < tol and np.abs(p2[1] - s_ymax) < tol 
                         and s_xmin-tol <= p1[0] <= s_xmax+tol)
                    )
                    if on_source:
                        self.interface_edges.append(([indices[i], indices[j]], edge_len))
            else:
                indices = self.connectivity[index]

            # --- ELEMENTAL CALCULATIONS ---
            axial = self.axial_length
            b, c, area = self._calculate_triangle(triangle_coordinates)
            grid = np.ix_(indices, indices)

            # Determine Material Properties
            is_source = triangle.intersects(self.source)
            temp_dep = self.source_dependence if is_source else self.domain_dependence
            h_cap = self.source_capacity if is_source else self.domain_capacity

            # 1. Heat Generation & Face Cooling (Out-of-Plane)
            if is_source:
                # Volumetric Heating
                heat_per_node = self.heating * axial * area / 3
                for i in indices:
                    self.load_vector[i] += heat_per_node

                # Face Cooling (simulates 10mm thickness cooling into the 3rd dimension)
                # h * Area * (T - T_inf)
                h_conv = self.convection
                ke_face = (h_conv * area / 12) * np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
                fe_face = (h_conv * self.boundary_temp * area / 3) * np.array([1, 1, 1])
                self.m_stiffness[grid] += ke_face
                self.load_vector[indices] += fe_face

            # 2. Stiffness Matrix (Conduction)
            u_elem = current_solution[indices] if current_solution is not None else self.boundary_temp
            k_temp = np.interp(np.mean(u_elem), temp_dep[0], temp_dep[1])
            
            local_b = np.array([b, c]) / (2 * area)
            ke_cond = k_temp * axial * area * np.dot(local_b.T, local_b)
            self.m_stiffness[grid] += ke_cond

            # 3. Mass Matrix (Thermal Inertia) - Only once
            if not self.constructed:
                me_local = h_cap * axial * (area / 12) * np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
                self.m_mass[grid] += me_local

        # --- GLOBAL CONVECTION ASSEMBLY (Boundary + Interface) ---
        h, T_inf = self.convection, self.boundary_temp
        for edge_indices, length in (self.boundary_edges + self.interface_edges):
            ke_conv = (h * length * axial / 6) * np.array([[2, 1], [1, 2]])
            fe_conv = (h * T_inf * length * axial / 2) * np.array([1, 1])

            grid_edge = np.ix_(edge_indices, edge_indices)
            self.m_stiffness[grid_edge] += ke_conv
            self.load_vector[edge_indices] += fe_conv

        if not self.constructed:
            self.connectivity = np.array(conductivity_map)
            self.constructed = True

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
