"""
Filename: main.py
Author: William Bowley

Description:
    Transient thermal solver for the 2D heat equation PDE
    using picounits to show unit-boundary abstractions.
    
    NOTE:
    This is a demonstration model and is not intended to 
    match a refined finite element solver
    
    NOTE:
    This example uses these dependencies matplotlib and shapely.
    To install run the command: pip install matplotlib shapely
"""

from typing import Any

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from solver import Builder, Mesher, solver
from picounits import LENGTH, MILLI, POWER, TEMPERATURE, TIME, DIFFUSIVITY

# Redefine sematic to SI metric naming
ms = 1 * MILLI * TIME
mm = 1 * MILLI * LENGTH
watt = POWER

# Parameters
boundary = 100 * mm
heat_length = 35 * mm
heat_height = 35 * mm
time_step = 1 * ms
power_density = 10 * MILLI * watt / mm ** 2
diffusion = 1.11e-2 * DIFFUSIVITY

# Builds the domain and the central heat-source
heat_location = ((boundary-heat_length) / 2, (boundary-heat_height) / 2)

domain = Builder.create_rectangle((0 * mm, 0 * mm), boundary, boundary)
heat_source = Builder.create_rectangle(heat_location, heat_length, heat_height)

# Meshes geometry and than solves it
mesher = Mesher(domain, heat_source)
problem_solver = solver(mesher)
problem_solver.build(power_density, 273.15 * TEMPERATURE)

fig, ax = plt.subplots(figsize=(6, 6))

# Initial frame solve
solution_now = problem_solver.solve_frame(time_step, diffusion)

# Initial plot
nodes, triangles = problem_solver.unique_nodes, problem_solver.connectivity
tpc = ax.tripcolor(
    nodes[:, 0], nodes[:, 1], triangles, solution_now,
    shading='gouraud', cmap='RdYlBu_r', vmin=273.15, vmax=1000
)
fig.colorbar(tpc, label='Temperature (K)')

ax.set_xlabel(f"Length ({boundary.unit})")
ax.set_ylabel(f"Height ({boundary.unit})")
ax.set_aspect('equal')
ax.set_title("Transient Heat Diffusion")


current_time_val = 0 * ms
ax.set_title(f"Transient Heat Diffusion - Time : {current_time_val:.3f}")

def update(frame: Any):
    """ Updates the Transient solution over time"""
    global solution_now, current_time_val
    _ = frame

    solution_now = problem_solver.solve_frame(time_step, diffusion, last_frame=solution_now)

    current_time_val += time_step
    ax.set_title(f"Thermal Diffusion | Time: {current_time_val:.3f}")

    tpc.set_array(solution_now)
    return tpc, ax.title

ani = animation.FuncAnimation(fig, update, frames=100, interval=time_step.value, blit=False)

plt.show()