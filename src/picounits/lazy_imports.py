"""
Filename: lazy_imports.py
Author: William Bowley
Version: 0.1

Description:
    This file defines a generic lazy import
    helper function and a specific import for
    factory as its the main lazy import.
"""


from typing import Any
from functools import lru_cache


class LazyImportError(ImportError):
    """ Exception for failed lazy imports """
    def __init__(self, caller: str, module: str):
        """ Returns a custom error message for lazy imports """
        msg = (
            f"Could not import '{module}' for '{caller}'. "
            "This usually means picounits was not installed correctly"
        )
        super().__init__(msg)


@lru_cache(maxsize=None)
def import_factory(caller_name: str) -> Any:
    """ Caches/returns the 'Factory' import route for lazy imports """
    try:
        from picounits.core.quantities.factory import Factory
        return Factory

    except ImportError:
        raise LazyImportError(caller_name, "Factory") from None


@lru_cache(maxsize=None)
def lazy_import(
    module_path: str, method_name: str, caller_name: str
) -> Any:
    """ 
    Caches/returns the module_path.module_name for lazy imports 
    """
    try:
        mod = __import__(module_path, fromlist=[method_name])
        return getattr(mod, method_name)

    except ImportError:
        raise LazyImportError(caller_name, method_name) from None
