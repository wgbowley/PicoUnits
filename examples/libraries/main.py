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
from picounits.extensions.loader import DynamicLoader

def print_loader_tree(
    loader: DynamicLoader, name="Root", indent="", is_last=True
) -> None:
    """
    Recursively prints the structure of the materials.uiv as a tree.
    """
    connector = "└── " if is_last else "├── "

    print(f"{indent}{connector}{name}")

    new_indent = indent + ("    " if is_last else "│   ")

    attrs = loader.attributes()
    items = list(attrs.items())

    for i, (key, value) in enumerate(items):
        last_item = (i == len(items) - 1)

        if isinstance(value, DynamicLoader):
            print_loader_tree(value, key, new_indent, last_item)
        else:
            leaf_connector = "└── " if last_item else "├── "
            print(f"{new_indent}{leaf_connector}{key}: {value}")

if __name__ == "__main__":
    p = Parser.open("examples/libraries/materials.uiv")
    print_loader_tree(p, name="materials.uiv")
