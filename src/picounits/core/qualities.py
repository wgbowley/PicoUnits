"""
Filename: qualities.py
Author: William Bowley
Version: 0.3

Description:
    This file defines the 'Quantity' class
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.constants import DIMENSIONLESS


@dataclass(slots=True)
class Quantity:
    """
    Represents a quantity within the library with both magnitude and unit
    """
    magnitude: Any
    unit: Unit
