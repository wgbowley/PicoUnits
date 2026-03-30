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
    This example uses these dependencies:
    To install run the command: pip install matplotlib shapely
"""

from typing import Any
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from engine import PreProcessor, Solver

from picounits import LENGTH as m, TIME as s
from picounits.extensions.parser import Parser


# File paths
BASE_DIR = Path(__file__).parent.parent.parent
library = BASE_DIR / "examples/solver/parameters.uiv"

params = Parser.open(library)

# Build simulation domain and heat source geometry
s_x, s_y = params.source.origin
domain = PreProcessor.rectangle((0*m, 0*m), params.problem.length, params.problem.height)
source = PreProcessor.rectangle((s_x, s_y), params.source.length, params.source.height)

# Meshes the geometry
preprocessor = PreProcessor(domain, source)
problem_solver = Solver(preprocessor)
problem_solver.build(params)

fig, ax = plt.subplots(figsize=(6, 6))

# Initial frame solve
solution_now = problem_solver.solve()

# Initial plot
nodes, triangles = problem_solver.unique_nodes, problem_solver.connectivity
tpc = ax.tripcolor(
    nodes[:, 0], nodes[:, 1], triangles, solution_now,
    shading='gouraud', cmap='RdYlBu_r', vmin=273.15, vmax=500
)
fig.colorbar(tpc, label='Temperature (K)')

ax.set_xlabel(f"Length ({params.problem.length.unit})")
ax.set_ylabel(f"Height ({params.problem.height.unit})")
ax.set_aspect('equal')
ax.set_title("Transient Heat Diffusion")

# Draws the source to the plot
xs, ys = problem_solver.source.exterior.xy
ax.plot(xs, ys, 'k', lw=1.5, label='Heat Source')
ax.legend(loc='upper right')

current_time_val = 0 * s
ax.set_title(f"Transient Heat Diffusion - Time : {current_time_val:.3f}")

def update(frame: Any):
    """ Updates the Transient solution over time"""
    global solution_now, current_time_val
    _ = frame

    solution_now = problem_solver.solve(solution_now)
    current_time_val += params.problem.time_step
    ax.set_title(f"Thermal Diffusion | Time: {current_time_val:.3f}")

    tpc.set_array(solution_now)
    return tpc, ax.title

ani = animation.FuncAnimation(
    fig, update, frames=100, interval=params.problem.time_step.value, blit=False
)
plt.show()