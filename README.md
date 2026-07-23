<!-- 
Color palette: 
#006d77ff, 
#d92c2aff 
-->
 
<p align="center">
  <a href="https://github.com/wgbowley/PicoUnits">
    <img src="media\picounit_logo.png" alt="PicoUnits logo">
  </a>
</p>
<p align="center">A dimensional constraint system for computational engineering.</p>
<p align="center">
  Define the dimensional environment of your application.<br>
  Keep physical meaning attached to computation.
</p>

---
 
![License](https://img.shields.io/badge/License-MIT-E14F4C?style=flat-square)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-006D77?style=flat-square)
[![PyPI Downloads](https://img.shields.io/pepy/dt/picounits?label=downloads\&style=flat-square\&color=E14F4C)](https://pepy.tech/projects/picounits)
 
> [!NOTE]
> PicoUnits is the dimensional environment underlying `PyFea`, `PicoMaterials`, and other cross-domain engineering projects.
 
## Overview
 
PicoUnits is a dimensional constraint system for computational engineering.
  
Unlike general-purpose unit libraries, PicoUnits separates:
 
- The underlying algebraic structure of a physical quantity.
- Prefixes represent scale along an existing dimensional axis.
- The symbols used to represent dimensions and derived units belong to the application's `unit frame`.

### Features
 
> [!important]
> - Pluggable unit systems via `Unit Frames` (domain-specific base dimensions)
> - Algebra-first unit system: no implicit or explicit unit conversion
> - Prefixes are representational and do not participate in unit algebra
> - Configuration format: `.uiv` and `.ut` with embedded validation
> - Boundary validation via `@expects`
> - Full numeric support: real, complex, and vector quantities

## Not a Unit Conversion Library
 
PicoUnits was never intended or designed as a universal unit conversion system.
 
It does not attempt to answer:
 
```text
3 metres → ? feet
```
 
Instead, it answers questions such as:
 
```text
- Does this quantity have the required dimensions?
- Are these two physical quantities algebraically compatible?
- Can this solver safely consume this value?
```
 
## What is a unit frame?
 
A unit frame defines the dimensional environment used by an application.
 
For example:
 
```text
[symbols]
time: s
length: m
mass: kg
current: A
TEMPERATURE: K
amount: mol
luminosity: cd
dimensionless: ∅
```
 
The underlying dimensional basis is independent of the notation used to represent it. The notation is simply a semantic layer applied over the same mathematical rules.
 
## What are .uiv & .ut?
 
Both are dimensionally aware formats. `.ut (unit types)` encodes custom base units for your system and `.uiv (unit informed values)` encodes value:unit pairs:
 
### `.ut`
 
```
# Coilgun Units - Derived from Base Dimensions (kg, m, s, etc.)
[version]
format: 0.1.0
 
[units]
ρ: kg/m^3
V: kg*m^2*s^-3*A^-1
```
 
### `.uiv`
 
All `value : unit` pairs exist in the form value `prefix(unit)`, for example:
 
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
 
# Value without prefix (volts - empty prefix)
voltage: 18 (V)         # Equivalent to ""(V)
current_limit: 40 (A) 
time_steps: 50 u(s)
atmospheric_density: 1.225 (ρ)
```
 
## Quick Start
 
```py
from picounits import expects, VOLTAGE, CURRENT, RESISTANCE
 
@expects(VOLTAGE)
def ohm_law(i, r):
    return i * r
 
# Correct usage
v = ohm_law(10 * CURRENT, 5 * RESISTANCE) 
print(v) # Output: 50.0 (kg·m²·s⁻³·A⁻¹) (Derived units need to be pulled in via .ut)
 
# This would raise a DimensionError:
# 'ohm_law' returned kg²·m⁴·s⁻⁶·A⁻³, expected kg·m²·s⁻³·A⁻¹ 
```
 
## Installation 
 
To install:
```bash
# Recommended for most users
pip install PicoUnits
```
or use `setuptools` locally:
 
```bash
git clone https://github.com/wgbowley/PicoUnits.git
cd PicoUnits
pip install -e .
```
 
## Documentation
 
> [!NOTE]
> Documentation is available in [`docs/`](docs/), with a standard introduction example available in [`examples/`](examples/).
