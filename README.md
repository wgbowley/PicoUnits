<p align="center">
  <img src="media/picounit_logo.png" alt="PicoUnits" style="max-width:600px;">
</p>

<p align="center">A runtime dimensional environment and unit-aware DSL for scientific computing in Python</p>


## PicoUnits: Usage
<!-- NOTE: Python version needs to checked before release, I am not sure the specific version  -->
![Python Version](https://img.shields.io/badge/python-3.10+-900001)
![License](https://img.shields.io/badge/license-MIT-D7DFE1)

Picounit is a dimensional environment designed for scientific computing specifically computational science. Key features:

- **Pluggable unit systems**:  Define custom base dimensions `(Unit Frames)` for your domain
- **Configuration format**:  `.uiv` files with embedded, validated units & `.ut` for unit types
- **Boundary validation**:  `@unit_validator` decorators catch errors at function interfaces
- **Full numeric support**:  Real, complex, and array-based vectors


But instead of talking about it, let's see some examples:

```py
>>> from PicoUnits import MILLI, LENGTH
>>> 12 * MILLI * LENGTH + 10 * LENGTH
>>> 10.012 (m)
```

As expected, it returns 10.01 meters, but what is a unit? A more exotic feature of PicoUnits is that its fundamental units are fully abstract. We call this the user's "Unit Frame"; by default, it's SI metric, but it could be astronomical units:

```py
# With a custom .picounit file defining light-years as LENGTH:
>>> from PicoUnits import MILLI, LENGTH
>>> 12 * MILLI * LENGTH + 10 * LENGTH
>>> 10.012 (ly)
```

All depends on the users `.picounit` file, which can be generated via the command `PicoUnits generate`. Another feature is the ability to use the `.ut` (unit types) and `.uiv` (unit-informed values) formats, which PicoUnits loads in via recursive attribute injection. So instead of a nested list, you get a wonderful object-based loader.

```yaml
[version]
format: 0.1.0
unit_frame: units.ut

[model]
voltage: 18 (V)  # volts
current_limit: 40 (A) 
time_steps: 50 u(s)
```

Your `.picounit` file defines your Unit Frame, your `.ut` defines any derived units and your `.uiv` files defines value:unit pairs. This ensures consistency-you can't accidentally load a config file expecting SI metric when your code is running in natural units.

```py
>>> from PicoUnits.parser import Parser
>>> p = Parser(parameters.uiv)
>>> p.model.voltage
>>> 18 (V)
```

Well, we’ve looked at simple calculations, changing unit frames, and importing units. But what about dimensional checks? Well, the main one is the `unit_validator`, which is a decorator that checks dimensionally out of a function. Let's intentionally pass wrong units to see what happens:

```py
>>> from PicoUnits import unit_validator, VOLTAGE, IMPEDANCE, CURRENT
>>> @unit_validator(VOLTAGE)
>>> def calculate_voltage(current, impedance):
>>>   return current * impedance
>>> 
>>> calculate_voltage((10+1j) * CURRENT ** 2, 10 * IMPEDANCE)
>>> DimensionError: 'calculate_voltage' returned kg·m²·s⁻³, expected kg·m²·s⁻³·A⁻¹
```

The `unit_validator` checks the dimensionality of the output to ensure it matches the expected type. It's very useful when prototyping as it compartmentalizes dimensional checking, decreasing mental overhead. 

**For a complete worked example**, see the <a style="color: #861211" href="examples/coilgun/">multi-stage coilgun simulation</a>
 which uses PicoUnits for electromagnetic physics calculations.

## Documentation 
Full documentation is available at <a style="color: #861211" href="/docs/">docs</a>, and simple to advanced examples are available at <a style="color: #861211" href="/examples/">examples</a>


### Installation
To install, simply:
```bash
pip install PicoUnits
```
or use setuptools locally:

```bash
git clone https://github.com/wgbowley/PicoUnits.git
cd PicoUnits
pip install -e .
```
 
