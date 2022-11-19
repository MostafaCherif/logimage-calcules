from utils import list_to_horizontal_str, list_to_vertical_str
from logimage import Logimage
import tkinter as tk


def create_window(logimage: Logimage):
    win = tk.Tk()
    MAX_HEIGHT = 600  # 500 for the logimage, 100 for the constraints
    MAX_WIDTH = 600  # 500 for the logimage, 100 for the constraints
    LOG_WIDTH = logimage.width
    LOG_HEIGHT = logimage.height

    # TODO: add support for non-squared logimages and adjust the place taken by the constraints

    canvas = tk.Canvas(win, width=MAX_WIDTH + 1, height=MAX_HEIGHT + 1)
    canvas.create_line(0, 100, MAX_WIDTH, 100, width=2)
    canvas.create_line(100, 0, 100, MAX_HEIGHT, width=2)

    # TODO: change constraints alignment from centered to left- and bottom-aligned (for instance)
    # or even allow the user to change

    for vline_index in range(LOG_WIDTH):
        if vline_index % 5 == 4:
            canvas.create_line(100 + (1 + vline_index) * 500/LOG_WIDTH,
                               0, 100 + (1 + vline_index) * 500/LOG_WIDTH, 600, width=2)
        else:
            canvas.create_line(100 + (1 + vline_index) * 500/LOG_WIDTH,
                               0, 100 + (1 + vline_index) * 500/LOG_WIDTH, 600)
        canvas.create_text(100 + (0.5 + vline_index) * 500 /
                           LOG_WIDTH, 15, text=list_to_vertical_str(logimage.top_constraints[vline_index]), anchor="n")

    for hline_index in range(LOG_HEIGHT):
        if hline_index % 5 == 4:
            canvas.create_line(0, 100 + (1 + hline_index) * 500 /
                               LOG_HEIGHT, 600, 100 + (1 + hline_index) * 500/LOG_HEIGHT, width=2)
        else:
            canvas.create_line(0, 100 + (1 + hline_index) * 500 /
                               LOG_HEIGHT, 600, 100 + (1 + hline_index) * 500/LOG_HEIGHT)
        canvas.create_text(15, 100 + (0.5 + hline_index) * 500 /
                           LOG_HEIGHT, text=list_to_horizontal_str(logimage.left_constraints[hline_index]), anchor="w")
    canvas.pack()
