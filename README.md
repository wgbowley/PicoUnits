<!-- Color palette: #006d77ff, #d92c2aff -->
<p align="center">
  <a href="https://github.com/wgbowley/PicoUnits">
    <img src="media\picounit_logo.png" alt="PicoUnits logo">
  </a>
</p>
<p align="center">A runtime dimensional environment and unit-aware DSL for scientific computing in Python</p>

---
> [!note]
> Picounits is the dimensional environment for `pyfea` and its included material library `pyfea-materials`.  

## Overview
<!-- NOTE: Python version needs to checked before release, I am not sure the specific version  -->
![License](https://img.shields.io/badge/License-MIT-E14F4C?style=flat-square&logoColor)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-006D77?style=flat-square)
[![PyPI Downloads](https://img.shields.io/pepy/dt/picounits?label=downloads&style=flat-square&color=E14F4C)](https://pepy.tech/projects/picounits)

PicoUnits is a dimensional correctness system for simulation pipelines. It enforces algebraic consistency at runtime within a fixed unit frame,
eliminating implicit conversion errors and cross-domain ambiguity in numerical models.
  
Unlike general-purpose unit libraries (e.g. Pint), PicoUnits separates:
- dimensional structure (units)
- scalar scaling (prefixes)
- numerical simulation semantics

This design prioritizes deterministic behaviour in numerical solvers and simulation pipelines over strict SI-algebra equivalence.
As a result, prefixes are resolved at construction time and do not participate in unit algebra or exponentiation.

### Features

> [!important]
> - Pluggable unit systems via Unit Frames (domain-specific base dimensions)
> - Algebra-first unit system: no implicit or explicit unit conversion
> - Prefixes are representational and do not participate in unit algebra
> - Configuration format: `.uiv` and `.ut` with embedded validation
> - Boundary validation via `@unit_validator`
> - Full numeric support: real, complex, and vector quantities

## What are .uiv & .ut?

Both are dimensionally aware formats. `.ut (unit types)` encodes custom base units for your system and `.uiv (unit informed values)` encodes value:unit pairs:

```
# Coilgun Units - Derived from Base Dimensions (kg, m, s, etc)
[version]
format: 0.1.0

[units]
ρ: kg/m^3
V: kg*m^2*s^-3*A^-1
```

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
voltage: 18 (V)
current_limit: 40 (A) 
time_steps: 50 u(s)
atmospheric_density: 1.225 (ρ)
```

## Quick Start

```py
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

## Installation 

> [!Important]
> Full documentation is available at [docs](/docs/), and beginner to advanced examples are available at [examples](/examples/)

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
 
