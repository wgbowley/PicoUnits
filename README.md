<p align="center">
  <img src="https://raw.githubusercontent.com/wgbowley/PicoUnits/release/media/picounit_logo.png" alt="PicoUnits">
  <br>
  <br>
  <em>Explicit units and dimensional analysis for scientific Python – Built with Correctness by <a style="color: #861211" href="https://github.com/wgbowley">William Bowley</a></em>
</p>


## Overview

**Current status (January 2026)**  
> The active, and installable version of PicoUnits is on the **`release`** branch.  
> All the code, examples (including the multi-stage coilgun simulation), documentation, packaging files (`pyproject.toml`, `setup.py`), and full README are there.

### Where to go next

Jump to the **release branch** for everything: <a style="color: #861211" href="https://github.com/wgbowley/PicoUnits/tree/release">picounits/release</a>

- Full README with usage examples, features, and philosophy  
- Source code in `src/picounits/`  
- Practical examples in `examples/`  
- Docs in `docs/` 
- Ready-to-install setup files  

(Once stabilized, this main branch will be updated with the merged/final code.)

> [!NOTE]
> PyPI is currently not the supported install path. Use manual installation via setup.py from the release branch instead. (No official release yet.)

### Quick peek
<!-- NOTE: Python version needs to checked before release, I am not sure the specific version  -->
![Python Version](https://img.shields.io/badge/python-3.10+-red)
![License](https://img.shields.io/badge/license-MIT-white)

Picounit is a zero-dependency Python package that does dimensional analysis at runtime. Key features:

- **Pluggable unit systems**:  Define custom "Unit Frames" for your domain
- **Configuration format**:  `.uiv` files with embedded, validated units  
- **Boundary validation**:  `@unit_validator` decorators catch errors at function interfaces
- **Full numeric support**:  Real, complex, and array-based vectors

But instead of talking about it, let's see some examples:

```py
>>> from picounits import MILLI, LENGTH
>>> 12 * MILLI * LENGTH + 10 * LENGTH
>>> RealPacket(value=10.012, unit=<Unit: m>)
```

As expected it returns 10.012 meters but what about dimensional checking? PicoUnits does runtime dimesional analysis alongside mathematical functions. As such dimensionally can be checked at boundaries such as through the `unit_validator`:

```py
>>> from picounits import unit_validator, VOLTAGE, IMPEDANCE, CURRENT
>>> @unit_validator(VOLTAGE)
>>> def calculate_voltage(current, impedance):
>>>   return current * impedance
>>>
>>> calculate_voltage((10+1j) * CURRENT ** 2, 10 * IMPEDANCE)
>>> ValueError: calculate_voltage returned kg·m²·s⁻³, expected kg·m²·s⁻³·A⁻¹
```

The `unit_validator` checks the dimensionality of the output to ensure it matches the expected type. It's very useful when prototyping as it compartmentalizes dimensional checking, decreasing mental overhead. 
