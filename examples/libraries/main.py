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
    """ Recursively prints the structure of the .uiv file as a tree. """
    connector = "└── " if is_last else "├── "
    print(f"{indent}{connector}{name}")
    new_indent = indent + ("    " if is_last else "│   ")

    attrs = loader.attributes()
    items = list(attrs.items())

    for index, (key, value) in enumerate(items):
        last_item = index == len(items) - 1
        leaf_connector = "└── " if last_item else "├── "

        if isinstance(value, DynamicLoader):
            print_loader_tree(value, key, new_indent, last_item)

        elif isinstance(value, (list, tuple)):
            # Format lists nicely
            if len(value) <= 4:
                print(f"{new_indent}{leaf_connector}{key}: {value}")
            else:
                print(f"{new_indent}{leaf_connector}{key}: [")

                for i, v in enumerate(value):
                    item_connector = "└── " if i == len(value) - 1 else "├── "
                    print(f"{new_indent}    {item_connector}{v}")
                print(f"{new_indent}    ]")

        else:
            print(f"{new_indent}{leaf_connector}{key}: {value}")

if __name__ == "__main__":
    p = Parser.open("examples/libraries/materials.uiv")
    print_loader_tree(p, name="materials.uiv")

    # Iron/Copper mix 70%/30%
    iron_density = p.pure_iron.physical.density
    copper_density = p.pure_copper.physical.density

    density = iron_density * 7/10 + copper_density * 3 / 10
    print(f"70 % Iron 30% Copper density: {density!r}")
