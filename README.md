<p align="center">
  <img src="media/PicoUnit_logo.png" alt="PicoUnits" style="max-width:600px;">
  <br>
  <br>
  <em>Explicit units and dimensional analysis for scientific Python – Built with Correctness by <a style="color: #861211" href="https://github.com/wgbowley">William Bowley</a></em>
  
</p>

---


Writing experimental physics models? Need to check dimensions at boundaries? Annoyed by vague configuration files? Picounits might be what you're looking for. 

Picounits is a lightweight dimensional analysis library and DSL for writing dimensionally explicit Python code.  Picounits support real numbers, complex numbers, and arrays based vectors. It is also a custom DSL called `.uiv` (unit-informed values), which allows for explicit units in configuration or reference libraries.



## Picounits: Usage
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
>>> RealPacket(value=10.01, unit=<Unit: m>)
```

As expected, it returns 10.01 meters, but what is a unit? A more exotic feature of Picounits is that its fundamental units are fully abstract. We call this the user's "Unit Frame"; by default, it's SI metric, but it could be astronomical units:

```py
# With a custom .picounit file defining light-years as LENGTH:
>>> from picounits import MILLI, LENGTH
>>> 12 * MILLI * LENGTH + 10 * LENGTH
>>> RealPacket(value=10.01, unit=<Unit: ly>)
```

All depends on the users `.picounit` file, which can be generated via the command `picounits generate`. Another feature is the ability to use the `.uiv` (unit-informed values) format, which picounits loads in via recursive attribute injection. So instead of a nested list, you get a wonderful object-based loader.

```yaml
[model]
voltage: 18 (kg*m^2*s^-3*A^-1)  # volts
current_limit: 40 (A) 
time_steps: 50 u(s)
```

Your `.picounit` file defines both your Unit Frame *and* what units your `.uiv` files can parse. This ensures consistency-you can't accidentally load a config file expecting SI metric when your code is running in natural units.

```py
>>> from picounits.parser import Parser
>>> p = Parser(parameters.uiv)
>>> print(p.model.voltage)
>>> 18 (kg·m²·s⁻³·A⁻¹)
```

Well, we’ve looked at simple calculations, changing unit frames, and importing units. But what about dimensional checks? Well, the main one is the `unit_validator`, which is a decorator that checks dimensionally out of a function. Let's intentionally pass wrong units to see what happens:

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

**For a complete worked example**, see the <a style="color: #861211" href="examples/coilgun/">multi-stage coilgun simulation</a>
 which uses PicoUnits for electromagnetic physics calculations.

## Documentation 
Full documentation is available at <a style="color: #861211" href="/docs/">docs</a>, and simple to advanced examples are available at <a style="color: #861211" href="/examples/">examples</a>


### Installation
To install, simply:
```bash
pip install picounits
```
or use setuptools locally:

```bash
git clone https://github.com/wgbowley/picounits.git
cd picounits
pip install -e .
```