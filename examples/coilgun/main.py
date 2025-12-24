"""
Filename: main.py
Author: William Bowley
Version: 0.1

Description:
    Analytical lumped-parameter coil-gun
    model using picounits to ensure correctness
"""

from math import pi
import matplotlib.pyplot as plt

from equations import (
    inductor_voltage, rk_2nd_order_current, position_b_field, inst_force,
    clipping_current
)

from picounits.extensions.parser import Parser
from picounits.constants import (
    TIME, VELOCITY, LENGTH, CURRENT, VOLTAGE, DIMENSIONLESS, 
    MAGNETIC_PERMEABILITY
)


p = Parser.open("examples/coilgun/parameters.uiv")

# Set calculations
relative = p.projectile.relative_perm
permeability = relative * 4 * pi * 1e-7 * MAGNETIC_PERMEABILITY

turns_per_meter = p.coil.turns / p.coil.axial_length
average_radius = (p.coil.outer_radius + p.coil.inner_radius) / 2

# Global accumulators for plotting
total_time_data = []
total_velocity_data = []
cumulative_time = 0.0 * TIME

initial_velocity = 0.0 * VELOCITY
results = []

for stage in range(p.model.number_stages.magnitude):
    time = 0.0 * TIME
    position = 0.0 * LENGTH
    velocity = initial_velocity
    current = 0.0 * CURRENT
    voltage = 0.0 * VOLTAGE
    direction = 1 * DIMENSIONLESS

    while position < p.coil.axial_length:
        supply_voltage = 0.0 * VOLTAGE
        if position < 0.5 * p.coil.axial_length:
            supply_voltage = p.model.voltage

        # Calculates the inductor voltage, then inductor current & limiting
        voltage = inductor_voltage(supply_voltage, current, p.coil.resistance)
        current = rk_2nd_order_current(
            current, voltage, p.coil.inductance,
            p.coil.resistance, p.model.time_steps
        )
        current = clipping_current(p.model.current_limit, current)

        # Calculates b-field strength, then force on projectile
        b_field = position_b_field(
            position, current, turns_per_meter, p.coil.axial_length,
            average_radius, permeability
        )

        # Ensures directionally flips due to the Flux Law
        if current.magnitude > 0:
            direction = 1 * DIMENSIONLESS
        else:
            direction = -1 * DIMENSIONLESS

        force = inst_force(
            b_field, permeability, p.projectile.radius, direction
        )

        # Calculates acceleration (f = ma)
        inst_acceleration = force / p.projectile.mass

        # Euler integration for velocity and position
        velocity += inst_acceleration * p.model.time_steps
        position += velocity * p.model.time_steps
        time += p.model.time_steps

        # Appends cumulative and velocity for plotting (Removes units)
        _time = cumulative_time + time
        _time = _time.to_base()
        _velocity = velocity.to_base()
        total_time_data.append(_time.magnitude)
        total_velocity_data.append(_velocity.magnitude)

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
    cumulative_time += time
    initial_velocity = velocity_exit

# Plot combined velocity vs time for all stages
plt.plot(total_time_data, total_velocity_data)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title(f'Velocity vs. Time for All {p.model.number_stages.magnitude} Stages')
plt.grid(True)
plt.show()