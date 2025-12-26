"""
Filename: config.py
Author: William Bowley
Version: 0.1
Clean: N

Description:
    Automatically finds and loads .picounits
    file from working dictionary.
"""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from typing import Dict
from warnings import warn

from picounits.configuration.picounits import (
    DEFAULT_ORDER, DEFAULT_SYMBOLS
)

# Cache effective preferences after first load
_effective_symbols: Dict[str, str] | None = None
_effective_order: Dict[str, int] | None = None


def _find_picounits_file() -> Path | None:
    """Search upwards from cwd for .picounits"""
    cwd = Path.cwd()
    for path in [cwd, *cwd.parents]:
        candidate = path / ".picounits"
        if candidate.is_file():
            return candidate
    return None


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

    return custom_order


def _load_from_file(filepath: Path) -> tuple[Dict[str, str], Dict[str, int]]:
    """Parse [symbols] and [order] sections from .picounits"""
    config = ConfigParser(delimiters=(":", "="), comment_prefixes=("#", ";"))
    config.read(filepath, encoding="utf-8")

    return _import_symbols(config), _import_order(config)


def _load_config() -> None:
    """ Loads the configuration """
    global _effective_symbols, _effective_order
    local_file = _find_picounits_file()

    if local_file:
        try:
            symbols, order = _load_from_file(local_file)
            _effective_symbols = {**DEFAULT_SYMBOLS, **symbols}
            _effective_order = order
            print(f"picounits: Loaded project config from {local_file}")
            return
        except Exception as e:
            warn(
                f"picounits: Failed to parse {local_file}, using defaults: {e}"
            )

    # No file or failed use defaults
    _effective_symbols = DEFAULT_SYMBOLS.copy()
    _effective_order = DEFAULT_ORDER.copy()
    print("picounits: No .picounits found, using standard SI units")


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


def reload_config() -> None:
    """ reloads configuration """
    global _effective_symbols, _effective_order
    _effective_symbols = None
    _effective_order = None
    _load_config()
