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

    def _get_path(self, parts):
        """ Navigates to a path and returns the object """
        obj = self
        for part in parts:
            if not hasattr(obj, part):
                return None
            obj = getattr(obj, part)
        return obj

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

    def find_and_replace(self, path: str, new_value: Any) -> bool:
        """ Finds a specific path and replaces its value. """
        parts = path.split('.')

        # Navigate to parent
        if len(parts) == 1:
            # Top-level attribute
            if hasattr(self, parts[0]):
                setattr(self, parts[0], new_value)
                return True
            return False

        # Navigate to parent of target
        parent = self._get_path(parts[:-1])
        if parent is None:
            return False

        # Replace the final attribute
        if hasattr(parent, parts[-1]):
            setattr(parent, parts[-1], new_value)
            return True

        return False

    def find_and_add(self, path: str, value: Any) -> bool:
        """ Adds a new path with the given value. """
        parts = path.split('.')
        self._set_path(parts, value)
        return True

    def attributes(self):
        """ Creates a dictionary of direct attributes"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

    def keys(self):
        """ Returns the single key or list of keys within that node """
        keys_list = list(self.attributes().keys())
        if len(keys_list) == 1:
            return keys_list[0]
        return keys_list

    def values(self):
        """ Returns the single value object directly """
        values_list = list(self.attributes().values())
        if len(values_list) == 1:
            return values_list[0]
        return values_list

    def __repr__(self):
        """ Returns the loaders direct members """
        items = ', '.join(self.keys())
        return f'Data({items})'

    def __getattr__(self, name: str) -> Any:
        """Allow dynamic attribute access"""
        raise AttributeError(
            f"'{type(self).__name__}' has no attribute '{name}'"
        )
