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
        """ Ensures data stays in the correct category """
        for key, value in dictionary.items():
            parts = key.split('.')
            self._set_path(parts, value)

    def _set_path(self, parts, value):
        """ Loads values via attribute injection """
        obj = self
        for part in parts[:-1]:
            if not hasattr(obj, part):
                setattr(obj, part, self.__class__({}))
            obj = getattr(obj, part)
        if isinstance(value, dict):
            setattr(obj, parts[-1], self.__class__(value))
        else:
            setattr(obj, parts[-1], value)

    @property
    def occupied(self) -> bool:
        """ Returns the state of the key pair """
        if len(self.__dict__) >= 1:
            return True
        return False

    def find(self, key, results=None):
        """ Finds key:value occurrences via recursion"""
        if results is None:
            results = []
        if hasattr(self, key):
            results.append({key: getattr(self, key)})
        # Recursion find
        for attr_value in self.__dict__.values():
            if isinstance(attr_value, self.__class__):
                attr_value.find(key, results)
        # Rebuilds a dict to reinsert into a loader structure
        items = {}
        for sub_results in results:
            for key, value in sub_results.items():
                items[key] = value
        return self.__class__(items)

    def attributes(self):
        """ Creates a dictionary of direct attributes"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

    def keys(self):
        """ Returns a list of keys within that node """
        return list(self.attributes().keys())

    def __repr__(self):
        """ Returns the loaders direct members """
        items = ', '.join(self.keys())
        return f'Data({items})'

    def __getattr__(self, name: str) -> Any:
        """Allow dynamic attribute access"""
        raise AttributeError(
            f"'{type(self).__name__}' has no attribute '{name}'"
        )
