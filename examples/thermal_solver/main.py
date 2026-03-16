"""
Filename: main.py
Author: William Bowley

Description:
    Transient thermal solver for the 2D heat equation PDE
    using picounits to show unit-boundary abstractions.
    
    NOTE:
    This is a demonstration model and is not intended to 
    match a refined finite element solver
    
    NOTE:
    This example uses these dependencies matplotlib and shapely.
    To install run the command: pip install matplotlib shapely
"""

from solver import Builder, Mesher
from picounits import LENGTH, MILLI, POWER

# Redefine sematic to SI metric naming
mm = 1 * MILLI * LENGTH
watt = POWER

# Parameters
boundary = 100 * mm
heat_length = 35 * mm
heat_height = 35 * mm
power_density = 10 * watt / mm ** 2
print(power_density)
# Builds the domain and the central heat-source
heat_location = ((boundary-heat_length) / 2, (boundary-heat_height) / 2)

domain = Builder.create_rectangle((0 * mm, 0 * mm), boundary, boundary)
heat_source = Builder.create_rectangle(heat_location, heat_length, heat_height)

# Meshes geometry and than solves it
mesh = Mesher(domain, heat_source)
