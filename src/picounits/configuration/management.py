"""
Filename: config.py

Description:
    Automatically finds and loads .picounits
    file from working dictionary.
"""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Any

from picounits.configuration.picounits import (
    DEFAULT_ORDER, DEFAULT_SYMBOLS
)


# Effective preferences after first load
_effective_symbols: Dict[str, str] | None = None
_effective_order: Dict[str, int] | None = None
_effective_derived: Dict[str, Any] = {}


def get_base_symbols() -> Dict[str, str]:
    """ Gets the base symbol from config """
    if _effective_symbols is None:
        _load_config()

    return _effective_symbols


def get_base_order() -> Dict[str, int]:
    """ Gets the base order from config """
    if _effective_order is None:
        _load_config()

    return _effective_order

def get_derived_units() -> Dict[str, Any]:
    """ Gets the derived units from config.  """
    return _effective_derived


def reload_config() -> None:
    """ reloads configuration """
    global _effective_symbols, _effective_order
    _effective_symbols, _effective_order = None, None

    _load_config()


def _load_config() -> None:
    """ Loads the configuration """
    global _effective_symbols, _effective_order
    local_file = _find_picounits_file()

    if local_file:
        try:
            symbols, order = _load_from_file(local_file)
            _effective_symbols = {**DEFAULT_SYMBOLS, **symbols}
            _effective_order = order
            return

        except Exception as e:
            raise RuntimeError(
                f"picounits: Failed to parse {local_file}, using defaults: {e}"
            ) from e

    # No file or failed use defaults
    _effective_symbols = DEFAULT_SYMBOLS.copy()
    _effective_order = DEFAULT_ORDER.copy()


def _find_picounits_file() -> Path | None:
    """ Search upwards from cwd for .picounits """
    cwd = Path.cwd()
    for path in [cwd, *cwd.parents]:
        # Search for exact filename in subtree
        candidate = path / ".picounits"
        if candidate.is_file():
            return candidate

    # Returns none for no results
    return None


def _load_from_file(filepath: Path) -> tuple[Dict[str, str], Dict[str, int]]:
    """ Parse [symbols] and [order] sections from .picounits """
    config = ConfigParser(delimiters=(":", "="), comment_prefixes=("#", ";"))
    config.read(filepath, encoding="utf-8")

    return _import_symbols(config), _import_order(config)


def _import_symbols(config: dict) -> Dict[str, str]:
    """ Loads the symbol dictionary """
    symbols: Dict[str, str] = {}
    if "symbols" in config:
        symbols: Dict[str, str] = {}

        for key, value in config["symbols"].items():
            clean_key = key.strip().upper()
            clean_value = value.strip()

            # Skips empty lines
            if clean_key:
                symbols[clean_key] = clean_value

        return symbols

    # Returns an empty dictionary when `[symbols]` is missing
    return symbols


def _import_order(config: dict) -> Dict[str, int]:
    """ Loads the order dictionary """
    custom_order: dict[str, int] = {}
    if "order" in config:
        for key, value_str in config["order"].items():
            clean_key = key.strip().upper()
            if not clean_key:
                continue
            try:
                value = int(value_str.strip())
            except ValueError as e:
                msg = f"Invalid order value '{value_str}' for '{key}"
                raise ValueError(msg) from e

            # If successfully parsed to integer
            custom_order[clean_key] = value
        return custom_order

    # Returns an empty dictionary when `[order]` is missing
    return custom_order


def add_derived_units(registry: Dict[str, Any]) -> None:
    """Gets the derived unit registry if a .ut file exists."""
    global _effective_derived
    if _effective_derived:
        msg = (
            "Only one .ut file can be imported at once. "
            f"Already contains {len(_effective_derived)} units."
        )
        raise RuntimeError(msg)

    if not registry:
        # Return if registry is empty
        _effective_derived = {}
        return

    # Adds registry to the derived units dictionary
    _effective_derived = registry.copy()
