"""
Filename: main.py
Author: William Bowley
Version: 0.1

Description:
    Analytical lumped-parameter coil-gun
    model using picounits to ensure correctness

    NOTE:
    This is an analytical, lumped-parameter demonstration model.
    It is Not intended to match FEM or experimental results.
    Its purpose is to demonstrate safe unit-aware numerical loops.

    NOTE:
    This example uses the dependency matplotlib to graph results.
    To install run the command: pip install matplotlib 
"""

from math import pi
from sys import exit
from matplot import plot
from equations import (
    inductor_voltage, rk_2nd_order_current, position_b_field, 
    inst_force, clipping_current, projectile_drag, projectile_mass, 
    estimate_turns, cal_resistance, cal_inductance
)

from picounits.extensions.parser import Parser
from picounits.constants import (
    TIME, VELOCITY, LENGTH, CURRENT, VOLTAGE, DIMENSIONLESS,
    MAGNETIC_PERMEABILITY, FLUX_DENSITY
)

p = Parser.open("examples/coilgun/parameters.uiv")

# Set calculations
relative = p.projectile.relative_perm
permeability = relative * 4 * pi * 1e-7 * MAGNETIC_PERMEABILITY
average_radius = (p.coil.outer_radius + p.coil.inner_radius) / 2

turns = estimate_turns(
    p.coil.axial_length, p.coil.inner_radius, p.coil.outer_radius,
    p.coil.wire_diameter, p.coil.fill_factor
)
turns_per_meter = turns / p.coil.axial_length
resistance = cal_resistance(
    turns, average_radius, p.coil.wire_diameter, p.coil.resistivity
)
inductance = cal_inductance(turns, p.coil.axial_length, average_radius)
mass = projectile_mass(
    p.projectile.axial_length, p.projectile.radius, p.projectile.density
)

# Global accumulators for plotting
total_time_data = []
total_force_data = []
total_velocity_data = []
total_position_data = []

cumulative_time = 0.0 * TIME
cumulative_position = 0.0 * LENGTH

initial_velocity = 0.0 * VELOCITY
results = []

for stage in range(p.model.number_stages.magnitude):
    time = 0.0 * TIME
    position = 0.0 * LENGTH
    velocity = initial_velocity
    current = 0.0 * CURRENT
    voltage = 0.0 * VOLTAGE
    b_prev = 0.0 * FLUX_DENSITY
    direction = 1 * DIMENSIONLESS
    b_gradient = 0 * (FLUX_DENSITY / TIME)

    while position < p.coil.axial_length:
        supply_voltage = 0.0 * VOLTAGE
        direction = 1 * DIMENSIONLESS
        # Switches voltage source off half way through the coil
        if position < 0.5 * p.coil.axial_length:
            supply_voltage = p.model.voltage

        # Mimics the pull back force as b_field is decreasing on exit
        if b_gradient.strip() < 0:
            direction = -1 * DIMENSIONLESS

        # Calculates the inductor voltage, then inductor current & limiting
        voltage = inductor_voltage(
            supply_voltage, current, resistance, 0 * VOLTAGE
        )
        current = rk_2nd_order_current(
            current, voltage, inductance, resistance,
            p.model.time_steps
        )
        current = clipping_current(p.model.current_limit, current)

        # Calculates b-field strength, then force on projectile
        b_now = position_b_field(
            position, current, turns_per_meter, p.coil.axial_length,
            average_radius, permeability, p.projectile.magnetic_saturation
        )

        force = inst_force(b_now, permeability, p.projectile.radius, direction)
        force += projectile_drag(
            velocity, p.model.atmospheric_density,
            p.projectile.coefficient_drag, p.projectile.radius
        )

        # Calculates acceleration (f = ma)
        inst_acceleration = force / mass

        # Euler integration for velocity and position
        velocity += inst_acceleration * p.model.time_steps
        delta_p = velocity * p.model.time_steps

        position += delta_p
        time += p.model.time_steps

        # Calculates the dB/dt
        area = pi * p.projectile.radius ** 2
        b_gradient = (b_now - b_prev) / p.model.time_steps
        b_prev = b_now

        # Appends cumulative and velocity for plotting (Removes units)
        cumulative_position += velocity * p.model.time_steps

        cumulative_time += p.model.time_steps
        total_time_data.append(cumulative_time.strip())

        total_force_data.append(force.strip())
        total_velocity_data.append(velocity.strip())
        total_position_data.append(cumulative_position.strip())
        # exit()
    velocity_exit = velocity
    delta_v = velocity_exit - initial_velocity

    results.append({
        "Stage": stage + 1,
        "Entry Speed:": initial_velocity,
        "Exit Speed:": velocity_exit,
        "Transit Time:": time,
        "DeltaV:": delta_v,
    })

    print(
        f"Stage {stage + 1}: entry={round(initial_velocity, 3)}, "
        f"exit={round(velocity_exit, 3)}, transit={round(time, 3)}"
    )

    # Update cumulative time and initial velocity for next stage
    initial_velocity = velocity_exit

# Plot combined velocity vs time for all stages
plot(
    total_time_data, total_position_data, total_force_data, total_velocity_data
)
