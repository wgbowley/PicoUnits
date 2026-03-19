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
    This example uses these dependencies:
    To install run the command: pip install matplotlib shapely
"""


from pathlib import Path
from engine import PreProcessor

from picounits import LENGTH as m
from picounits.extensions.parser import Parser


# File paths
BASE_DIR = Path(__file__).parent.parent.parent
library = BASE_DIR / "examples/solver/parameters.uiv"

params = Parser.open(library)

# Build simulation domain and heat source geometry
s_x, s_y = params.source.origin
domain = PreProcessor.rectangle((0*m, 0*m), params.problem.length, params.problem.height)
source = PreProcessor.rectangle((s_x, s_y), params.source.length, params.source.height)

# Meshes the geometry
preprocessor = PreProcessor(domain, source)

