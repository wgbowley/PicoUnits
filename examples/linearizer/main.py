"""
Filename: main.py
Author: William Bowley

Description:
    Example of a thermistor linearizer based on 
    SBOA323A by Texas Instruments.

    Calculates the resistors needed to produce
    a linear output voltage over a temperature
    range.
"""

from math import exp

from picounits.core import unit_validator, Quantity as q
from picounits import IMPEDANCE, VOLTAGE, TEMPERATURE, KILO, MILLI

# Thermistor Steinhart-Hart Inverse Coefficients
A1 = -14.6337
B1 = 4791.84
C1 = -115334
D1 = -3.7305e+06

# Circuit Variables
SUPPLY = 3.3 * VOLTAGE
V_OUT_MAX = 3.2 * VOLTAGE
V_OUT_MIN = 100 * MILLI * VOLTAGE

MAX_TEMPERATURE = 125 * TEMPERATURE
MIN_TEMPERATURE = 25 * TEMPERATURE

NTC100AT25C = 100 * KILO * IMPEDANCE

# Standard value for the feedback resistor
FEEDBACK = 1.5 * KILO * IMPEDANCE


@unit_validator(IMPEDANCE)
def calculate_ntc_resistance(temp_celsius: q) -> q:
    """ Calculates the NTC thermistor resistance using Steinhart-Hart """
    tk = temp_celsius.value + 273.15
    exponent_value = (A1 + (B1 / tk) + (C1 / tk ** 2) + (D1 / tk ** 3))

    return NTC100AT25C * exp(exponent_value)


@unit_validator(VOLTAGE)
def voltage_range(low_side_ntc) -> tuple[q]:
    """ Calculates the input voltage range, minium and maximum """
    def calculation(temp_res):
        """ Calculation for voltage depends on different temp res"""
        return SUPPLY * (low_side_ntc / (temp_res + low_side_ntc))

    return calculation(R_NTC_MIN), calculation(R_NTC_MAX)


@unit_validator(IMPEDANCE)
def ref_divider_resistance(
    v_in_max: q, ideal_gain: q, divider: q
) -> tuple[q]:
    """ Calculates the resistance of the high_side and low_side resistors """
    high_side = FEEDBACK * SUPPLY / (v_in_max * ideal_gain - V_OUT_MAX)
    low_side = divider * high_side / (high_side - divider)
    return high_side, low_side


# Calculated values for resistance at max temp and min temp
R_NTC_MAX = calculate_ntc_resistance(MAX_TEMPERATURE)
R_NTC_MIN = calculate_ntc_resistance(MIN_TEMPERATURE)

low_side = (R_NTC_MIN * R_NTC_MAX) ** 0.5
v_in_min, v_in_max = voltage_range(low_side)

ideal_gain = (V_OUT_MAX - V_OUT_MIN) / (v_in_max - v_in_min)
ref_divider = FEEDBACK / (ideal_gain - 1)
ref_high, ref_low = ref_divider_resistance(v_in_max, ideal_gain, ref_divider)
actual_gain = (ref_divider + FEEDBACK) / ref_divider


print("============================")
print(f"Resistance at {MIN_TEMPERATURE.value} c is {R_NTC_MIN:.3f}")
print(f"Resistance at {MAX_TEMPERATURE.value} c is {R_NTC_MAX:.3f}")
print("============================")

# Print out names based partly on naming in the schematic present in (SBOA323A)
print(f"Low side NTC divider (R1) = {low_side:.3f}")
print(f"Low side reference divider (R2) = {ref_low:.3f}")
print(f"High side reference divider (R3) = {ref_high:.3f}")
print("============================")
print(f"Op Amp feedback (R4) = {FEEDBACK:.3f}")
print(f"Op Amp gain = {actual_gain:.3f}")
print("============================")
