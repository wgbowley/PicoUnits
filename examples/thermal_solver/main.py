"""
Filename: main.py

Description:
    Thermostatic solver for the 2D heat equation PDE
    using picounits for correctness, shapely for topology
    and matplotlib for display.
    
    NOTE:
    This is a demonstration model and is not intended to match
    finite element solver. Its purpose is to demonstrate safe
    unit-aware input at boundaries into PDE loops.
"""

import numpy as np
import matplotlib.pyplot as plt

from shapely.geometry import Polygon, MultiPoint
from shapely.ops import triangulate


coords = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
boundary = Polygon(coords)

x_coords, y_coords = np.linspace(0, 5, 10), np.linspace(0, 5, 10)
points = MultiPoint([(x, y) for x in x_coords for y in y_coords])

triangles = triangulate(points)

clipped_mesh = [t for t in triangles if t.within(boundary)]

# Finds nodes within the mesh
nodes = []
for triangles in clipped_mesh:
    nodes.extend(list(triangles.exterior.coords))

unique_nodes = np.unique(nodes, axis=0)
num_nodes = len(unique_nodes)

# Finds the elements from number of triangles
num_elements = len(clipped_mesh)

# Load vector due to 0 heat source its all zeros
load_vector = np.zeros(num_nodes)

# TO DO:
# Need to calculate the global stiffness matrix ke=a*(B^t*B)
# Need to inform boundary conditions such as u=400k and u=273.15k
# Solve using conjugate gradient solver.


# 5. Plotting with Matplotlib
fig, ax = plt.subplots(figsize=(6, 6))

for tri in clipped_mesh:
    x, y = tri.exterior.xy
    ax.fill(x, y, alpha=0.3, fc='cyan', ec='blue', lw=0.5)

ax.set_aspect('equal')
plt.title("Thermal Mesh")
plt.show()