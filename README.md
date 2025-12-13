<p align="center">
  <img src="media/banner.png" alt="PicoUnits" style="max-width:600px;">
  <br>
  <em>SI Unit System Designed For Minimal Overhead  – Built with speed by <a href="https://github.com/wgbowley">William Bowley</a></em>
</p>

## Overview

![Work in Progress](https://img.shields.io/badge/status-wip-orange)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**PicoUnits** is a low overhead library designed for ensuring dimensional accuracy during runtime. It uses a custom seven fundamental unit system based off the standard SI metric fundamental units. 

```py
class SIBase(Enum):
    """ SI metric fundamental units expect mass is defined as a gram """
    SECOND = auto()             # Time
    METER = auto()              # Length
    GRAM = auto()               # Mass
    AMPERE = auto()             # Electric Current
    KELVIN = auto()             # Temperature
    MOLE = auto()               # Amount of a substance
    CANDELA = auto()            # Luminous Intensity
    DIMENSIONLESS = auto()      # Non-physical quantity
```

Each unit is made up of a subclass called `Dimension` which itself is made of two sub-dataclasses `SIBase`, `PrefixScale` and one integer value `exponent`:

```py
@dataclass()
class Dimension:
    """
    Defines a SI metric dimension through 'SIBase', 'PrefixScale and 'exponent'
    """
    prefix: PrefixScale = PrefixScale.BASE
    base: SIBase = SIBase.DIMENSIONLESS
    exponent: int = 1

class Unit:
    """
    Defines a SI metric unit composed of a singular or multiple 'Dimension'.
    """
    def __init__(self, *dimensions: Dimension) -> None:
        self.dimensions = list(dimensions)
```



Each `Quantity` has both a magnitude and unit, and through the usage of dunder methods dimensional analysis happens in parallel with arithmetic operations.  

```py
@dataclass
class Quantity:
    """
    Represents a quantity within the framework with both magnitude and unit
    """
    magnitude: float | int
    unit: Unit
```

## Installation

PicoUnits requires Python 3.10 or newer.

```bash
pip install picounits
```
