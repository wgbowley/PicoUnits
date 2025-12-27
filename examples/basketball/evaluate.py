"""
Filename: evaluate.py
Author: William Bowley
Version: 0.2

Description:
    Analytical lumped-parameter model 3D
    projectile motion evaluation class
"""

from math import cos, sin

from equations import (
    ball_mass, calculate_displacement, ball_drag, force_vector
)

from picounits.constants import TIME, VELOCITY, FORCE, LENGTH
from picounits.extensions.parser import Parser
from picounits.extensions.loader import DynamicLoader
from picounits.core.quantities import Quantity as q


class _simulate:
    """ Simulates the basketball in 3D space """
    def __init__(
        self, name: int, loader: DynamicLoader, beta: q, alpha: q, mass: q
    ) -> None:
        """ Initiation of the simulation class """
        self.name = name
        self.loader = loader
        self.finished = False

        self.beta = beta
        self.alpha = alpha
        self.mass = mass

        # Backboard bounding box (aligned with axes)
        self.backboard_j = -self.loader.backboard.offset_behind_hoop
        self.tolerance = self.loader.ball.radius + self.loader.backboard.thickness / 2

        self.half_width = self.loader.backboard.width / 2 + self.loader.ball.radius
        center_k = self.loader.hoop.height
        half_height = self.loader.backboard.height / 2 + self.loader.ball.radius
        self.bottom_k = center_k - half_height
        self.top_k = center_k + half_height

        # Hoop center
        self.hoop = (0 * LENGTH, 0 * LENGTH, self.loader.hoop.height)

        # Post simulation variables
        self.end_position = (0.0, 0.0, 0.0)
        self.time = 0.0
        self.score = float('inf')
        self.position_data: list[tuple[float, float, float]] = []

    def _strip_vector(self, vector: tuple[q, q, q]) -> tuple[float, float, float]:
        """ Strips quantities off the vector """
        x, y, z = vector
        return x.strip(), y.strip(), z.strip()

    def _calculate_score(
        self, velocity: tuple[q, q, q], direction: tuple[q, q, q]
    ) -> float:
        """ Calculates the score of the ball in that position """
        vi, vj, vk = self._strip_vector(velocity)
        di, dj, dk = self._strip_vector(direction)

        # Calculates the dot product of the velocity and direction
        p_dot = vi * di + vj * dj + vk * dk

        # Calculates magnitude of velocity and direction
        v_mag = (vi ** 2 + vj ** 2 + vk ** 2) ** 0.5
        d_mag = (di ** 2 + dj ** 2 + dk ** 2) ** 0.5

        # Calculates the score, magnitude of direction removes dimensionally
        return (d_mag) ** 2 * (1 - p_dot / (v_mag * d_mag)) + (d_mag) ** 2

    def run(self) -> None:
        """ Runs the ball simulation """
        l = self.loader
        total_time = 0 * TIME
        pi, pj, pk = l.launch.i, l.launch.j, l.launch.k
        vi, vj, vk = 0 * VELOCITY, 0 * VELOCITY, 0 * VELOCITY

        above_floor = True
        while above_floor and total_time < l.model.timeout:
            displacement = calculate_displacement(
                (l.launch.i, l.launch.j, l.launch.k), (pi, pj, pk)
            )

            fi, fj, fk = 0 * FORCE, 0 * FORCE, 0 * FORCE
            if (
                displacement <= l.launch.acceleration_distance and
                total_time <= 1 * TIME
            ):
                # Launch phase happens for the first second if it fails, it drops
                fi, fj, fk = force_vector(l.launch.force, self.alpha, self.beta)

            di, dj, dk = ball_drag(
                (vi, vj, vk), 
                l.model.atmospheric_density,  l.ball.coefficient_drag, l.ball.radius
            )
            gk = self.mass * l.model.gravity

            ri, rj, rk = fi + di, fj + dj, fk + dk + gk
            ai, aj, ak = ri / self.mass, rj / self.mass, rk / self.mass

            vi += ai * l.model.time_step
            vj += aj * l.model.time_step
            vk += ak * l.model.time_step

            pi += vi * l.model.time_step
            pj += vj * l.model.time_step
            pk += vk * l.model.time_step

            prev_pj = pj
            pj += vj * l.model.time_step
            # Backboard collision
            if (
                prev_pj > self.backboard_j and pj <= self.backboard_j + self.tolerance
            ) or \
                (prev_pj < self.backboard_j and pj >= self.backboard_j - self.tolerance
            ):
                # Crossed or entered zone, and approaching
                if vj.magnitude < 0:
                    vj = -vj * self.loader.backboard.restitution
                    # Reflect position over plane
                    pj = self.backboard_j - (pj - self.backboard_j)

            # Log position
            self.position_data.append((pi.strip(), pj.strip(), pk.strip()))
            total_time += l.model.time_step

            direction_vector = (self.hoop[0]-pi, self.hoop[1]-pj, self.hoop[2]-pk)
            step_score = self._calculate_score((vi, vj, vk), direction_vector)
            if step_score < self.score:
                self.score = step_score

            if pk < 0 * LENGTH:  # hit floor
                above_floor = False
                self.finished = True

        if total_time > l.model.timeout:
            msg = "Failed to simulate ball trajectory"
            raise RuntimeError(msg)

        self.time = total_time
        self.end_position = pi, pj, pk

    @property
    def get_path(self) -> list[float, float, float]:
        """ Returns the path the ball took """
        if self.finished:
            return self.position_data

        raise RuntimeError(
            "Simulation must be ran first before requesting data"
        )

    @property
    def get_score(self) -> float:
        """ Returns the balls trajectory score """
        if self.finished:
            return self.score

        raise RuntimeError(
            "Simulation must be ran first before requesting data"
        )

    @property
    def get_report(self) -> str:
        """ Returns the simulation path """
        if self.finished:
            return (
                f"Name = {round(self.name, 3)}, "
                f"flight time = {round(self.time, 3)}, "
                f"final_position = {[round(i, 3) for i in self.end_position]} "
                f"Score = {round(q(self.score), 3)} "
            )

        raise RuntimeError(
            "Simulation must be ran first before requesting data"
        )

class Evaluate:
    """ Evaluation class for trial alpha/beta angles """
    def __init__(self, file_path: str) -> None:
        """ Initiation of the evaluation class """
        self.loader: DynamicLoader = Parser.open(file_path)

        self.ball_mass = ball_mass(
            self.loader.ball.radius, self.loader.ball.material_density
        )

        # Holds the ball path of each trial
        self.trial_paths: list[list] = []

    def trial(self, beta: float, alpha: float) -> float:
        """ Tries a new beta/alpha combination with error handling """ 
        name = len(self.trial_paths) + 1
        simulate = _simulate(name, self.loader, q(beta), q(alpha), self.ball_mass)

        try:
            simulate.run()
            # Print success report
            print(simulate.get_report)
            self.trial_paths.append(simulate.get_path)
            return simulate.score

        except RuntimeError:
            # If the ball gets stuck or times out, return '999.0' score
            print(
                f"Trial {name} Failed: Physics Timeout (Returning INF).. "
                "Retrying with new variables"
            )
            return 999.0

    def gen_hoop(self, num_points=64) -> list[tuple[float, float, float]]:
        """ Returns a series of points around the hoop """
        i_c, j_c, k_c = 0, 0, self.loader.hoop.height.strip()
        radius = self.loader.hoop.radius.strip()

        points = []
        for n in range(num_points):
            angle = 2 * 3.14159 * n / num_points
            i = i_c + radius * cos(angle)
            j = j_c + radius * sin(angle)
            points.append((i, j, k_c))
        return points

    def gen_backboard(self) -> list[tuple[float, float, float]]:
        """ Returns a series of vertices for the backboard """

        r = self.loader.ball.radius.strip()  # NOT hoop radius

        half_width = self.loader.backboard.width.strip() / 2 + r
        half_height = self.loader.backboard.height.strip() / 2 + r

        # Vertically centered on the hoop
        center_k = self.loader.hoop.height.strip()
        bottom_k = center_k - half_height
        top_k = center_k + half_height

        # Behind the hoop in -j direction
        front_j = -self.loader.backboard.offset_behind_hoop.strip() - r

        return [
            (-half_width, front_j, bottom_k),  # Bottom-Left
            ( half_width, front_j, bottom_k),  # Bottom-Right
            ( half_width, front_j, top_k),     # Top-Right
            (-half_width, front_j, top_k)      # Top-Left
        ]

    def gen_floor(self) -> list[tuple[float, float, float]]:
        """ Returns a series of vertices for the floor (k = 0 plane) """
        launch_i = self.loader.launch.i.strip()
        launch_j = self.loader.launch.j.strip()

        # Floor boundaries: from shooter to beyond hoop
        min_i, max_i = min(0, launch_i) - 10, max(0, launch_i) + 10
        min_j, max_j = min(0, launch_j) - 10, max(0, launch_j) + 10

        return [
            (min_i, min_j, 0.0),
            (max_i, min_j, 0.0),
            (max_i, max_j, 0.0),
            (min_i, max_j, 0.0)
        ]

    @property
    def paths(self) -> list[list]:
        """ Returns the balls different paths """
        return self.trial_paths
