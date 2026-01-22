"""
Filename: loader.py
Author: William Bowley
Version: 0.1

Description:
    Defines the dynamic loader for .uiv
    (Unit-Informed Values) files.
"""

from typing import Any


class DynamicLoader:
    """ Loads the values from the parser into attributes """
    def __init__(self, dictionary: dict[str, Any]) -> None:
        """ Loads values via attribute injection """
        for key, value in dictionary.items():
            # Removes 'dots' to ensure no errors
            key = key.replace('.', '_')

            if isinstance(value, dict):
                # Recursively converts nested dicts
                setattr(self, key, DynamicLoader(value))
            else:
                setattr(self, key, value)

    def find(self, key, results=None) -> dict:
        """ Finds key:value occurrences via recursion"""
        if results is None:
            results = []

        if hasattr(self, key):
            results.append(getattr(self, key))

        for attr_value in self.__dict__.values():
            if isinstance(attr_value, DynamicLoader):
                attr_value.find(key, results)

        return results

    def attributes(self) -> dict[str, Any]:
        """ Creates a dictionary of direct attributes"""
        attrs = {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
        return attrs

    def keys(self) -> list[str]:
        """ Returns a list of keys within that node """
        attrs = self.attributes()

        keys = []
        for key in attrs.keys():
            keys.append(key)

        return keys

    def __repr__(self) -> str:
        """ Returns the loaders direct members """
        attrs = self.attributes()

        # Formation of name as key=value pairs
        items = ', '.join(f'{key}' for key in attrs.keys())
        return f'Data({items})'

    def __getattr__(self, name: str) -> Any:
        """Allow dynamic attribute access"""
        raise AttributeError(
            f"'{type(self).__name__}' has no attribute '{name}'"
        )
