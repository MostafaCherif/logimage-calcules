from utils import list_to_horizontal_str, list_to_vertical_str
from nonogram import Nonogram
import tkinter as tk
from typing import Tuple


def create_window(nonogram: Nonogram):
    win = tk.Tk()
    LOG_WIDTH = nonogram.width
    LOG_HEIGHT = nonogram.height
    MAX_HEIGHT, MAX_WIDTH = get_nonogram_dimensions(LOG_HEIGHT, LOG_WIDTH)

    # TODO: add support for non-squared nonograms and adjust the place taken by the constraints

    canvas = tk.Canvas(win, width=MAX_WIDTH + 1, height=MAX_HEIGHT + 1)
    canvas.create_line(0, 100, MAX_WIDTH, 100, width=2)
    canvas.create_line(100, 0, 100, MAX_HEIGHT, width=2)

    # TODO: change constraints alignment from centered to left- and bottom-aligned (for instance)
    # or even allow the user to change

    for vline_index in range(LOG_WIDTH):
        if vline_index % 5 == 4:
            canvas.create_line(100 + (1 + vline_index) * (MAX_WIDTH - 100)/LOG_WIDTH,
                               0,
                               100 + (1 + vline_index) *
                               (MAX_WIDTH - 100)/LOG_WIDTH,
                               MAX_HEIGHT,
                               width=2)
        else:
            canvas.create_line(100 + (1 + vline_index) * (MAX_WIDTH - 100)/LOG_WIDTH,
                               0,
                               100 + (1 + vline_index) *
                               (MAX_WIDTH - 100)/LOG_WIDTH,
                               MAX_HEIGHT)

        canvas.create_text(100 + (0.5 + vline_index) * (MAX_WIDTH - 100) /
                           LOG_WIDTH,
                           15,
                           text=list_to_vertical_str(
                               nonogram.top_constraints[vline_index]),
                           anchor="n")

    for hline_index in range(LOG_HEIGHT):
        if hline_index % 5 == 4:
            canvas.create_line(0,
                               100 + (1 + hline_index) * (MAX_HEIGHT - 100) /
                               LOG_HEIGHT,
                               MAX_WIDTH,
                               100 + (1 + hline_index) * (MAX_HEIGHT - 100)/LOG_HEIGHT, width=2)
        else:
            canvas.create_line(0,
                               100 + (1 + hline_index) * (MAX_HEIGHT - 100) /
                               LOG_HEIGHT,
                               MAX_WIDTH,
                               100 + (1 + hline_index) * (MAX_HEIGHT - 100)/LOG_HEIGHT)

        canvas.create_text(15,
                           100 + (0.5 + hline_index) * (MAX_HEIGHT - 100) /
                           LOG_HEIGHT,
                           text=list_to_horizontal_str(
                               nonogram.left_constraints[hline_index]),
                           anchor="w")
    canvas.pack()


def get_nonogram_dimensions(log_height: int, log_width: int) -> Tuple[int, int]:
    """
    Constraints:
    - A 100*100 zone on the top left corner (that should be added to the normal result)
    - The grid zone should be at least 500px high and wide
    - Maximum 800px high, 1600px wide (possibility to contradict the previous rule)
    """
    height_width_ratio = log_height / log_width
    if height_width_ratio > 1.6:  # A 500px width would result in a >800px height
        return (800 + 100, 500 + 100)
    elif height_width_ratio < 0.3125:  # A 500px height would result in a >1600px width
        return (500 + 100, 1600 + 100)
    else:
        # both sides are at least 500px long
        scale_factor = 500 / min(log_height, log_width)
        return (100 + int(log_height * scale_factor), 100 + int(log_width * scale_factor))
