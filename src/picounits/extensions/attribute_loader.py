"""
Filename: attribute_loader.py

Description:
    Defines the `Loader` & `DynamicLoader` 
    for `.uiv` (unit-informed values) files.
"""


from __future__ import annotations

from typing import Any
from dataclasses import dataclass


class AttributeNotFound(AttributeError):
    """ Exception for attribute not found error """
    def __init__(self, attribute: str, path: str):
        """ Returns a custom error message """
        self.path = path
        self.attribute = attribute

        msg = f"'{attribute}' not found at '{path}' within loader tree"
        super().__init__(msg)


class InjectionError(Exception):
    """Raised when a value cannot be injected into a Loader tree."""
    def __init__(self, path: str, value: Any):
        self.path = path
        self.value = value

        msg = f"Failed to inject '{value}' at '{path}'"
        super().__init__(msg)


@dataclass(frozen=True, slots=True)
class LoaderContext:
    """ Stores the context of the loader structure """
    indent: str = ""
    in_last: bool = True
    inline: int = 4

    def next_level(self) -> LoaderContext:
        """ Creates context for the next level of nesting """
        new_indent = self.indent + ("    " if self.in_last else "│   ")
        return LoaderContext(new_indent, True, self.inline)

    def with_last(self, is_last: bool) -> LoaderContext:
        """ Creates context with updated last flag """
        return LoaderContext(self.indent, is_last, self.inline)

    def connector(self) -> str:
        """ Returns the tree connector character """
        return "└── " if self.in_last else "├── "


class Loader:
    """ Loads the values from the parser into attribute tree """
    def __init__(self, dictionary: dict[str, any], name: str | None = None) -> None:
        """ Ensures data stays in the correct category """
        self._name = name

        for key, value in dictionary.items():
            # Splits the path into keys -> e.i `vacuum.meta` -> ['vacuum', 'meta']
            path_items = key.split('.')
            self._set_path(path_items, value)

    def info(self, name: str = "root", inline: int = 4, context: LoaderContext = None) -> None:
        """ Recursively prints the structure of the loader as a tree. """
        if context is None:
            # Initialize context if not provided
            context = LoaderContext(inline=inline)

        if self._name is not None:
            # Use class name if available
            name = self._name

        # Print the current node within the tree
        connector = context.connector()
        print(f"{context.indent}{connector}{name}")

        # Begins routing for next node within the tree
        child_context = context.next_level()
        items = list(self._attributes().items())
        for index, (key, value) in enumerate(items):
            last_item = index == len(items) - 1
            self._print_child(key, value, child_context.with_last(last_item))

    def _print_child(self, key: str, value, context: LoaderContext) -> None:
        """ Prints a child node based on its type. """ 
        if isinstance(value, self.__class__):
            # Recursively print nested object
            value.info(key, inline=context.inline, context=context)
            return

        if isinstance(value, (list, tuple)):
            self._print_collection(key, value, context)
            return

        leaf_connector = context.connector()
        print(f"{context.indent}{leaf_connector}{key}: {value}")

    def _print_collection(self, key: str, collection, context: LoaderContext) -> None:
        """Prints a collection (list or tuple) with proper formatting."""
        leaf_connector = context.connector()
        # Print array in-line if within limit
        if len(collection) <= context.inline:
            print(f"{context.indent}{leaf_connector}{key}: {collection}")
            return

        # Prints arrays as multi-line objects
        print(f"{context.indent}{leaf_connector}{key}: [")
        for i, item in enumerate(collection):
            item_connector = "└── " if i == len(collection) - 1 else "├── "
            print(f"{context.indent}    {item_connector}{item}")

        print(f"{context.indent}    ]")

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
