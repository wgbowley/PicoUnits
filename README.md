<p align="center">
  <a href="https://github.com/wgbowley/PicoUnits">
    <img src="https://raw.githubusercontent.com/wgbowley/PicoUnits/main/media/picounit_logo.png" 
         alt="PicoUnits">
  </a>
</p>

<p align="center">A runtime dimensional environment and unit-aware DSL for scientific computing in Python</p>

## PicoUnits: Usage
<!-- NOTE: Python version needs to checked before release, I am not sure the specific version  -->
![Python Version](https://img.shields.io/badge/python-3.10+-900001)
![WIP](https://img.shields.io/badge/status-WIP-D7DFE1)
![License](https://img.shields.io/badge/license-MIT-900001)

Picounit is a dimensional environment designed for computational science. It serves to make simulation code
structurally correct and includes:

- **Pluggable unit systems**:  Define custom base dimensions `(Unit Frames)` for your domain
- **Configuration format**:  `.uiv` files with embedded, validated units & `.ut` for unit types
- **Boundary validation**:  `@unit_validator` decorators catch errors at function interfaces
- **Full numeric support**:  Real, complex, and array-based vectors

## What is .uiv & .ut?

Both are dimensionally aware formats, .ut (unit types) encodes custom base units for your system and .uiv (unit informed values) encodes value, unit pairs:

```
# Coilgun Units - Derived from Base Dimensions (kg, m, s, etc)
[version]
format: 0.1.0

[units]
ρ: kg/m^3
V: kg*m^2*s^-3*A^-1
```

All value : unit pairs exist in the form value prefix(unit), for example:

```
[version]
format: 0.1.0
unit_frame: units.ut

[notes]
# Analytical model for a multi-stage coil-gun
# Models electrical, magnetic and motional dynamics

[model]
number_stages: 10

# Millimeter -> prefix `m` and unit `m` hence prefix(unit), m(m)
stage_gap: 10 m(m)
voltage: 18 (V)
current_limit: 40 (A) 
time_steps: 50 u(s)
atmospheric_density: 1.225 (ρ)
```

## Quick Start

```python
from picounits import unit_validator, VOLTAGE, CURRENT, RESISTANCE

@unit_validator(VOLTAGE)
def ohm_law(i, r):
    return i * r

# Correct usage
v = ohm_law(10 * CURRENT, 5 * RESISTANCE) 
print(v) # Output: 50.0 (kg·m²·s⁻³·A⁻¹) (Derived units need to be pulled in via .ut)

# This would raise a DimensionError:
# ohm_law(10 * VOLTAGE, 5 * RESISTANCE)
```

## Documentation 
Full documentation is available at <a style="color: #861211" href="/docs/">docs</a>, and beginner to advanced examples are available at 
<a style="color: #861211" href="/examples/">examples</a>

## Installation
To install:
```bash
# Recommended for most users
pip install PicoUnits
```
or use setuptools locally:

```bash
git clone https://github.com/wgbowley/PicoUnits.git
cd PicoUnits
pip install -e .
```
 
