"""
Filename: plotting.py
Author: William Bowley
Version: 0.1

Description:
    Allows for plotting of complex numbers to the terminal
"""

from shutil import get_terminal_size

from picounits.constants import IMPEDANCE
from picounits.core.quantities.scalars.types.complex import (
    ComplexPacket as ComplexQuantity
)


def _draw_line(
    grid: list[list[str]], start: tuple[float, float], end: tuple[float, float]
) -> list[list[str]]:
    """Draws a line to the topology map using Bresenham's line algorithm. """

    # Convert to integers
    x0, y0 = map(int, start)
    x1, y1 = map(int, end)

    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1

    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1

    err = dx + dy

    # Calculates the maximum width of the grid
    max_y, max_x = len(grid) - 1, len(grid[0]) - 1

    while True:
        if 0 <= x0 < max_x and 0 <= y0 < max_y:
            # Avoids overwriting the axes
            if grid[y0][x0][0] == ' ':
                grid[y0][x0] = '·'

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx

        if e2 <= dx:
            err += dx
            y0 += sy

    return grid


def argand_plot(complex_numbers: list[ComplexQuantity]) -> None:
    """ Generates a argand diagram for complex quantity """
    width, height = get_terminal_size()
    width, height = width // 2, height // 2

    biggest = complex_numbers[0]
    for i in complex_numbers:
        if i.magnitude > biggest.magnitude:
            biggest = i

    # Checks for same units before plotting
    reference = complex_numbers[0]
    for i in range(1, len(complex_numbers)):
        reference.unit_check(complex_numbers[i].unit)

    # Strips quantity from the complex numbers
    numbers = [complex_number.value for complex_number in complex_numbers]
    reals, imags = [z.real for z in numbers], [z.imag for z in numbers]

    # Uses -2 / 2 to force the origin to be in the viewable area
    # Uses +5 Real to reverse space for labels, Uses +2 Img to prevent overlap
    min_real, max_real = min(*reals, -2) -3, max(*reals, 2) + 5
    min_imag, max_imag = min(*imags, -2) -2, max(*imags, 2) + 2

    # Defaults the grid to cells of ' '
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    def get_coords(re, im):
        """ Local function to generate plots """
        x = int((re - min_real) / (max_real - min_real) * (width - 1))
        y = int((im - min_imag) / (max_imag - min_imag) * (height - 1))
        return x, height - 1 - y

    def put_text(x, y, text):
        """ Local function to generate text points """
        for i, char in enumerate(text):
            if 0 <= x + i < width and 0 <= y < height:
                grid[y][x + i] = (char)

    ox, oy = get_coords(0, 0)
    for i in range(width): 
        grid[oy][i] = '─'
    for i in range(height): 
        grid[i][ox] = '│'

    grid[oy][ox] = '┼'

    text = f"Re {reference.unit}"
    put_text(width - len(text), oy, text)
    text = f"Im {reference.unit}"
    put_text(ox - len(text) // 2, 0, text)

    for z in numbers:
        px, py = get_coords(z.real, z.imag)

        # Line vector coordinates
        x0, y0, x1, y1 = ox, oy, px, py
        grid = _draw_line(grid, [x0, y0], [x1, y1])

        grid[py][px] = '●'
        text = f" {str(z).strip('()')}"
        put_text(px + 1, py, text)

    print("\n Argand Diagram")
    for row in grid: 
        print("".join(row))

argand_plot([(80+10j) * IMPEDANCE, (-88-10j) * IMPEDANCE])
