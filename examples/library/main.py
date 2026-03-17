"""
Filename: main.py
Author: William Bowley

Description:
    Example of using picounits to import a material 
    library with units. 
    
    This ensure correctness when parsing values into
    dimensional pipelines such as FEM or lumped parameter models.
"""

from pathlib import Path

from picounits import Quantity as Q, unit_validator, PRESSURE
from picounits.extensions.parser import Parser

# File paths
BASE_DIR = Path(__file__).parent.parent.parent
library = BASE_DIR / "examples/library/materials.uiv"
library_units = BASE_DIR / "examples/library/si_metric.ut"

materials = Parser.open(library, library_units)

# Shows library ontology
materials.tree("materials.uiv")
print("=== Derived parameters from library ===")


# Calculate mixture density of Iron/Copper mix 70%/30%
iron_density = materials.pure_iron.physical.density
copper_density = materials.pure_copper.physical.density

density = iron_density * 7/10 + copper_density * 3 / 10
print(f"70 % Iron 30% Copper density: {density!r}")


# Extract NdFeB grades for usage
@unit_validator(PRESSURE)
def _magnet_energy(br_hc: list[Q]) -> Q:
    """ Calculates the energy density of the magnet """
    remanence, coercivity = br_hc
    return 1/2 * remanence * coercivity

NdFeB = materials.NdFeB
n33, n35, = NdFeB.grades.N33, NdFeB.grades.N35
n33_d, n35_d = _magnet_energy(n33), _magnet_energy(n35)

print(f"Energy Density | N33: {n33_d:.3f}; N35: {n35_d:.3f}")


# Calculates the electrical resistivity of copper
resistivity = 1/materials.pure_copper.electrical.conductivity
print(f"Copper resistivity: {resistivity:.3f}")

print("=======================================")
