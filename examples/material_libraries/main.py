"""
Filename: main.py
Author: William Bowley
Version: 0.1

Description:
    Example of using picounits to import a material 
    library with units. 
    
    This ensure correctness when parsing values into
    dimensional pipelines such as FEM or lumped parameter models.
"""

from picounits.extensions.parser import Parser

p = Parser.open("examples/geometry/test.uiv")
print(p)