"""
Filename: matplot.py
Author: William Bowley
Version: 0.2

Description:
    Graphing script for the 3D projectile motion
    simulation and optimization using picounits
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from evaluate import Evaluate


def graph_results(evaluator: Evaluate) -> None:
    """ Graphs all trials, hoop, backboard, and floor """

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    # Adds the Floor at (k = 0 plane)
    floor_verts = evaluator.gen_floor()
    floor_poly = Poly3DCollection(
        [floor_verts],
        alpha=0.25,
        facecolors="#333333",
        edgecolors="none"
    )
    ax.add_collection3d(floor_poly)

    # Adds the backboard
    bb_verts = evaluator.gen_backboard()
    bb_poly = Poly3DCollection(
        [bb_verts],
        alpha=0.5,
        facecolors="white",
        edgecolors="gray"
    )
    ax.add_collection3d(bb_poly)

    # Adds the hoop
    hoop_points = evaluator.gen_hoop()
    hi, hj, hk = zip(*hoop_points)

    ax.plot(
        hi + (hi[0],),
        hj + (hj[0],),
        hk + (hk[0],),
        color="red",
        linewidth=4,
        label="Hoop Target"
    )

    # Plots all the ball trajectories
    paths = evaluator.paths
    for idx, path in enumerate(paths):
        pi, pj, pk = zip(*path)

        label = f"Trial {idx + 1}" if idx == len(paths) - 1 else None
        ax.plot(
            pi,
            pj,
            pk,
            color="#90D5FF",
            alpha=0.7,
            linewidth=1,
            label=label
        )


    # Axes, limits, camera
    ax.set_title("3D Basketball Optimization: All Trial Trajectories", fontsize=15)

    ax.set_xlabel("i (m) | Width")
    ax.set_ylabel("j (m) | Depth")
    ax.set_zlabel("k (m) | Height")

    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=25, azim=-60)

    if paths:
        ax.legend()

    plt.tight_layout()
    plt.show()
