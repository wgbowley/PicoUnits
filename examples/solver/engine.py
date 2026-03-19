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

from picounits import UnitError, Q, LENGTH, TEMPERATURE, POWER


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


class Solver:
    """ Solves the transient thermal PDE over 2D geometry using FEM """
    def __init__(self, preprocessor: PreProcessor) -> None:
        """ Initializes the solver """
        # Saves mesh and raw geometry for matrix assembly
        self.mesh = preprocessor.mesh
        self.domain = preprocessor.domain_coordinates
        self.source = preprocessor.source_box_coords

        # Calculates the number of nodes and elements
        nodes = []
        for triangle in self.mesh:
            nodes.append(list(triangle.exterior.coords))

        self.unique_nodes = np.unique(nodes, axis=0)
        self.number_nodes = len(self.unique_nodes)

        self.num_element = len(self.mesh)

        # Configures the load vector, mass and stiffness matrix
        self.load_vector = np.zeros(self.number_nodes)
        self.m_stiffness = np.zeros((self.number_nodes, self.number_nodes))
        self.m_mass = np.zeros((self.unique_nodes, self.unique_nodes))

        # Post init variables
        self.axial_length = 0
        self.volumetric_power = 0
        self.boundary_temperature = 0

        self.system = None
        self.connectivity = None

    def build(self, axial_length: Q, volumetric_power: Q, boundary_temp: Q) -> None:
        """ Builds the simulation domain via assembly of stiffness and mass matrixes """
        for item in (axial_length, volumetric_power, boundary_temp):
            if not isinstance(item, Q):
                msg = f"{item!r} must be {Q} not {type(item)!r}"
                raise UnitError(msg)

        if axial_length.unit != LENGTH:
            msg = f"{axial_length!r} must be in {LENGTH!r}"
            raise UnitError(msg)

        if volumetric_power.unit != POWER/LENGTH**3:
            msg = f"{volumetric_power!r} must be in {POWER/LENGTH**3!r}"
            raise UnitError(msg)

        if boundary_temp.unit != TEMPERATURE:
            msg = f"{boundary_temp!r} must be in {TEMPERATURE}"
            raise UnitError

        # Strips away units after validation
        self.axial_length = axial_length.stripped
        self.boundary_temperature = boundary_temp.stripped
        self.volumetric_power = volumetric_power.stripped

    