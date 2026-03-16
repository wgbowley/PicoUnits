
"""
Filename: solver.py
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

from picounits import Quantity as Q, LENGTH, MASS, TIME, TEMPERATURE


class Builder:
    """ Builds geometry """
    @staticmethod
    def create_rectangle(bottom_left: tuple[Q, Q], length: Q, height: Q) -> list:
        """ Creates a square vector geometry """
        x, y = bottom_left

        return [(x, y), (x + length, y + height)]


class Mesher:
    """ Builds than meshes the problem domain """
    @classmethod
    def _validate_geometry(cls, geometry: list[tuple[Q, Q]]) -> list:
        """ Checks units to ensure correctness of input geometry """
        raw_geometry = []
        for point in geometry:
            x, y = point

            if x.unit != LENGTH or y.unit != LENGTH:
                raise ValueError("Points must be defined in-terms of length")

            raw_geometry.append((x.value, y.value))

        return raw_geometry

    def __init__(self, domain: list, heat_source: list) -> list:
        """ Validates units and than builds domain """
        domain = self._validate_geometry(domain)
        heat = self._validate_geometry(heat_source)

        # Converts to shapely boxes
        heat_box = box(heat[0][0], heat[0][1], heat[1][0], heat[1][1])
        heat_box_coords = list(heat_box.exterior.coords)

        # Build grid around geometry
        bl, tr = domain[0], domain[1]
        x_coords, y_coords = np.linspace(bl[0], tr[0], 20), np.linspace(bl[1], tr[1], 20)
        points = MultiPoint([(x, y) for x in x_coords for y in y_coords])

        # Meshes the geometry
        all_points_list = [(p.x, p.y) for p in points.geoms] + heat_box_coords
        refined_points = MultiPoint(all_points_list)

        # Saves variables
        self.mesh = triangulate(refined_points)
        self.domain, self.heat = domain, heat
        self.heat_box = heat_box


class solver:
    """ Solves the meshed problem """
    def __init__(self, mesher: Mesher) -> None:
        """ Initializes the solver """
        self.mesh = mesher.mesh
        self.heat_box = mesher.heat_box
        self.heat_source = 0
        self.boundary_temperature = 0

        nodes = []
        for triangle in self.mesh:
            nodes.extend(list(triangle.exterior.coords))

        self.unique_nodes = np.unique(nodes, axis=0)
        self.num_nodes = len(self.unique_nodes)
        self.num_element = len(self.mesh)

        self.load_vector = np.zeros(self.num_nodes)
        self.K_global = np.zeros((self.num_nodes, self.num_nodes))
        self.M_global = np.zeros((self.num_nodes, self.num_nodes))
        self.connectivity = None

    def build(self, heat_source: Q, boundary_temperature: Q) -> None:
        """ Builds the domain for solving """
        if (
            heat_source.unit != MASS * TIME ** -3 or
            boundary_temperature.unit != TEMPERATURE
        ):
            raise ValueError(
                "Please use correct units for both heat source and temperature"
            )

        self.heat_source = heat_source.stripped
        self.boundary_temperature = boundary_temperature.stripped

    def _build_matrixes(self) -> None:
        """ Builds the stiffness and mass matrixes from mesh """
        con_map = []
        for triangle in self.mesh:
            triangle_coords = np.array(triangle.exterior.coords)[:3]

            # Map triangle nodes to their indices within unique nodes
            idx = []
            for point in triangle_coords:
                # Finds node position via minimal distance
                dists = np.linalg.norm(self.unique_nodes - point, axis=1)
                idx.append(np.argmin(dists))
            con_map.append(idx)

            # Breaks triangle nodes into coordinates
            x1, y1 = triangle_coords[0]
            x2, y2 = triangle_coords[1]
            x3, y3 = triangle_coords[2]

            # Uses coordinates to calculate (b,c) matrix and area
            b = [y2-y3, y3-y1, y1-y2]
            c = [x3-x2, x1-x3, x2-x1]
            area = 0.5 * abs(x1*b[0] + x2*b[1] + x3*b[2])

            # Local stiffness & map to global matrix
            local_b = np.array([b, c]) / (2 * area)
            ke_local = area * np.dot(local_b.T, local_b)

            # Local mass matrix
            a, b, c = [2, 1, 1], [1, 2, 1], [1, 1, 2]
            me_local = (area / 12) * np.array([a, b, c])

            for i in range(3):
                for j in range(3):
                    self.K_global[idx[i], idx[j]] += ke_local[i, j]
                    self.M_global[idx[i], idx[j]] += me_local[i, j]

            # Adds heat source to load vector
            if triangle.intersects(self.heat_box):
                heat_per_node = self.heat_source * triangle.area / 3
                for i in idx:
                    self.load_vector[i] += heat_per_node

        self.connectivity = np.array(con_map)

    def conjugate_gradient(
        self,
        A: np.ndarray,
        B: np.ndarray,
        initial: Q | None = None, 
        tolerance: float =1e-9,
        max_iter: int =1000
    ) -> Q:
        " Conjugate gradient solver for Ax = B linear system "
        sol = (
            initial.stripped if hasattr(initial, 'stripped')
            else np.zeros_like(B)
        )

        # Setup Initial Residuals
        r = B - np.dot(A, sol)
        p = r.copy()
        r_sold = np.dot(r, r)

        for _ in range(max_iter):
            Ap = np.dot(A, p)

            # Calculate step length alpha
            alpha = r_sold / np.dot(p, Ap)

            # Update solution and residual
            sol += alpha * p
            r -= alpha * Ap

            # Check convergence
            rs_new = np.dot(r, r)
            if np.sqrt(rs_new) < tolerance:
                break

            # Update search direction
            p = r + (rs_new / r_sold) * p
            r_sold = rs_new

        return sol * TEMPERATURE
