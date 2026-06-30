"""
Filename: loader.py

Description:
    Defines the `Loader` & `DynamicLoader` for 
    `.uiv` (unit-informed values) files.
"""

from typing import Any

from picounits.extensions.utilities.parser_errors import (
    AttributeNotFound, InjectionError
)


class Loader:
    """ Loads the values from the parser into attribute tree """
    def __init__(self, dictionary: dict[str, any], name: str | None = None) -> None:
        """ Ensures data stays in the correct category """
        self._name = name

        for key, value in dictionary.items():
            # Splits the path into keys -> e.i `vacuum.meta` -> ['vacuum', 'meta']
            path_items = key.split('.')
            self._set_path(path_items, value)

    def info(
        self, name="Root", indent="", is_last=True, inline_limit: int = 4
    ) -> None:
        """ Recursively prints the structure of the loader as a tree. """
        if self._name is not None:
            name = self._name
        
        connector = "└── " if is_last else "├── "
        print(f"{indent}{connector}{name}")

        new_indent = indent + ("    " if is_last else "│   ")
        attrs = self._attributes()
        items = list(attrs.items())
        for index, (key, value) in enumerate(items):
            last_item = index == len(items) - 1
            leaf_connector = "└── " if last_item else "├── "

            if isinstance(value, self.__class__):
                # Continues the recursion via entering the next loader structure
                value.info(key, new_indent, last_item)

            elif isinstance(value, (list, tuple)):
                if len(value) <= inline_limit:
                    # Print inline result
                    print(f"{new_indent}{leaf_connector}{key}: {value}")

                else:
                    # Print result vertically according to inline limit
                    print(f"{new_indent}{leaf_connector}{key}: [")
                    for i, v in enumerate(value):
                        item_connector = "└── " if i == len(value) - 1 else "├── "
                        print(f"{new_indent}    {item_connector}{v}")
                    print(f"{new_indent}    ]")

            else:
                print(f"{new_indent}{leaf_connector}{key}: {value}")

    def _set_path(self, path_items: Any, value: Any) -> None:
        """ Loads values via attribute injection """
        node = self

        # Iterates over the `path_keys` until the destination key (last key)
        for key in path_items[:-1]:
            if not hasattr(node, key):
                setattr(node, key, self.__class__({}, name=key))

            # Sets the new node as the node_attribute
            node = getattr(node, key)

        # Fall-back for parsing dictionaries into attribute tree
        if isinstance(value, dict):
            value = self.__class__(value)

        # Injects the value under the destination key (last key)
        setattr(node, path_items[-1], value)

    def _attributes(self) -> dict:
        attributes = {}
        # Iterates over the items within the node
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                attributes[key] = value

        return attributes

    def __getattr__(self, key: str) -> Any:
        """ Allow dynamic attribute access """
        raise AttributeNotFound(key, self._name)

    def __repr__(self):
        """ Returns the loaders direct members """
        attributes = self._attributes()

        items = ', '.join(attributes)
        if self._name is None:
            return f'Paths({items})'

        return f'{self._name}({items})'


class DynamicLoader(Loader):
    """ Searchable/Editable Attribute Tree based on `Loader` """
    def find(self, path: str) -> Any:
        """ Find sub-tree under requested path """
        node = self

        # Iterates over dotted path until sub-tree is found
        for key in path.split("."):
            if not hasattr(node, key):
                return None

            node = getattr(node, key)

        return node

    def inject(self, path: str, value: Any) -> None:
        """ Adds a new path with a given value """
        try:
            path_items = path.split('.')
            self._set_path(path_items, value)
        except:
            raise InjectionError(path, value) from None
