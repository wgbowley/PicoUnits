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

It provides the infrastructure to define, represent, validate, serialize, and enforce physical dimensions throughout engineering software and simulation pipelines.

Rather than treating units as metadata attached to numerical values, PicoUnits treats dimensional structure as part of the computational model.

```
Physical Model
        ↓
Unit frame & notation
        ↓
Parameter Files / Material Files
        ↓
Solver / simulation pipeline
        ↓
Outputs with Notation 
```

PicoUnits is designed for applications where physical quantities move between models, configuration files, numerical solvers, and engineering subsystems.

## The Idea

PicoUnits separates three concepts that are often coupled together computationally:

### Dimensional structure
The underlying algebraic structure of a physical quantity.

```text
Force = mass · length · time⁻²
```

### Scalar scaling

Prefixes represent scale along an existing dimensional axis.

```text
m(m)   → millimetre
u(s)   → microsecond
M(S_m) → megasiemens per metre
```

Prefixes are resolved at construction time and do not become part of dimensional algebra.

### Notation and semantics

The symbols used to represent dimensions and derived units belong to the application's **unit frame**.
A project can define its own dimensional vocabulary without changing the underlying dimensional system.
This allows PicoUnits to act as a **dimensional foundation**, rather than imposing a single global notation.

## Not a Unit Conversion Library

PicoUnits is intentionally not designed as a universal unit conversion system.

It does not attempt to answer:

```text
3 metres → ? feet
```

Instead, it answers questions such as:

```text
Does this quantity have the required dimensions?
Are these two physical quantities algebraically compatible?
Does this configuration value satisfy the model's dimensional contract?
Can this solver safely consume this value?
```

PicoUnits operates within a defined **unit frame**.

A unit frame establishes the dimensional basis and notation used by an application. Within that environment, dimensional relationships are explicit and deterministic.

## Unit Frames

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

The underlying dimensional basis is independent of how it is represented. The notation is a semantic layer. This allows the
same dimensional infrastructure to be used across different computational domain while keeping the notation domain specific.


## Dimensionally Aware Configuration

PicoUnits provides two domain-specific formats:

* `.ut` — **Unit Types**, defining a project's derived units and dimensional vocabulary.
* `.uiv` — **Unit-Informed Values**, defining configuration and physical data with dimensional information embedded directly in the data.

### `.ut`

A `.ut` file defines derived units for a project:

```text
[version]
format: 0.1.0

[Mechanics]
N:  kg*m*s^-2
J:  kg*m^2*s^-2
W:  kg*m^2*s^-3
Pa: kg*m^-1*s^-2

[Electricity]
V:   kg*m^2*s^-3*A^-1
S_m: kg^-1*m^-3*s^3*A^2

[magnetic]
T:   kg*s^-2*A^-1
Wb:  kg*m^2*s^-2*A^-1
A_m: A*m^-1
```

The dimensional definition is explicit and machine-readable.

### `.uiv`

A `.uiv` file embeds physical meaning directly into application data:

```text
[version]
format: 0.1.0
unit_frame: units.ut

[model]
number_stages: 10

stage_gap: 10 m(m)
voltage: 18 (V)
current_limit: 40 (A)
time_steps: 50 u(s)
atmospheric_density: 1.225 (ρ)
```

The result is configuration that is both **human-readable and dimensionally meaningful**.

Instead of:

```python
density = 1.225
voltage = 18
time_step = 0.00005
```

the physical meaning is represented directly:

```text
atmospheric_density: 1.225 (ρ)
voltage: 18 (V)
time_steps: 50 u(s)
```

The units are not comments documenting the data.

**They are part of the data contract.**

## Runtime Dimensional Constraints

Dimensional requirements can be enforced at computational boundaries using `@expects`.

```python
from picounits import expects, VOLTAGE, CURRENT, RESISTANCE

@expects(VOLTAGE)
def ohm_law(i, r):
    return i * r
```

Valid dimensional inputs satisfy the contract:

```python
v = ohm_law(
    10 * CURRENT,
    5 * RESISTANCE
)
```

Invalid dimensional inputs raise a `DimensionError` rather than silently producing a physically meaningless result:

```python
# Raises DimensionError
ohm_law(
    10 * VOLTAGE,
    5 * RESISTANCE
)
```

## Installation

```bash
pip install PicoUnits
```

Or install locally from source:

```bash
git clone https://github.com/wgbowley/PicoUnits.git
cd PicoUnits
pip install -e .
```

## Documentation
> [!IMPORTANT]
> Documentation is available in [`docs/`](docs/), with standard introduction example available in [`examples/`](examples/).
