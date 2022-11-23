import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from board import Board
from nonogram import board_to_nonogram
import numpy as np
from images_processing import grayscale_img, resize_img, to_board
from nonogramwindow import create_window

imPath = "test"

LINES_COUNT = 3
COLUMNS_COUNT = 3


root = tk.Tk()

insert_label = tk.Label(text="Ajoutez votre image ici")
insert_label.pack()

image = tk.Label()


def load_image_button_pressed():
    openImageFile()


def validation_button_pressed():
    global imPath, canvas_nonogram, LINES_COUNT, COLUMNS_COUNT
    LINES_COUNT = int(entry_horizontal.get())
    COLUMNS_COUNT = int(entry_vertical.get())
    board = board_from_image(imPath)
    draw_board_in_canvas(canvas_nonogram, board)


def nonogram_visualization_button_pressed():
    global imPath, canvas_nonogram, LINES_COUNT, COLUMNS_COUNT
    LINES_COUNT = int(entry_horizontal.get())
    COLUMNS_COUNT = int(entry_vertical.get())
    board = board_from_image(imPath)
    nonogram = board_to_nonogram(board)
    create_window(nonogram)


def openImageFile():
    global img, image, imPath
    imPath = filedialog.askopenfilename(initialdir=".", title="Open an image", filetypes=(
        ("Image file", "*.png"), ("Image file", "*.jpeg"), ("Image file", "*.jpg"), ("All File Types", "*.*")))
    if imPath:
        PILimg = Image.open(imPath)
        PILimg = PILimg.resize((200, 200))
        img = ImageTk.PhotoImage(PILimg)
        image.configure(image=img)


def draw_board_in_canvas(canvas: tk.Canvas, board: Board) -> None:
    global LINES_COUNT, COLUMNS_COUNT
    draw_lines()
    data = board.data.T
    for i, j in np.ndindex(data.shape):
        if data[i, j] == 1:
            canvas.create_rectangle(
                i * 200/LINES_COUNT, j * 200/COLUMNS_COUNT, (i + 1) * 200/LINES_COUNT, (j + 1) * 200/COLUMNS_COUNT, fill="#000")
        else:
            canvas.create_rectangle(
                i * 200/LINES_COUNT, j * 200/COLUMNS_COUNT, (i + 1) * 200/LINES_COUNT, (j + 1) * 200/COLUMNS_COUNT, fill="#fff")


def board_from_image(path: str):
    global slider, LINES_COUNT, COLUMNS_COUNT
    img = grayscale_img(path)
    img = resize_img(img, (LINES_COUNT, COLUMNS_COUNT))
    arr = np.array(img)
    board = to_board(arr, 255 - slider.get())
    return board


load_image_button = tk.Button(
    text="Choisissez une image...", command=load_image_button_pressed)
load_image_button.pack()

image.pack()

label_entry_horizontal = tk.Label(
    text="Entrez le nombre de lignes du nonogram")
entry_horizontal = tk.Entry(root)
label_entry_vertical = tk.Label(
    text="Entrez le nombre de colonnes du nonogram")
entry_vertical = tk.Entry(root)

label_entry_horizontal.pack()
entry_horizontal.pack()
label_entry_vertical.pack()
entry_vertical.pack()


slider = tk.Scale(from_=0, to=255, tickinterval=32,
                  length=250, orient="horizontal")
slider.pack()

validation_button = tk.Button(
    text="Valider", command=validation_button_pressed)
validation_button.pack()

canvas_nonogram = tk.Canvas(width=202, height=202)
canvas_nonogram.pack()

nonogram_visualization_button = tk.Button(
    text="Visualiser le nonogram vide", command=nonogram_visualization_button_pressed
)
nonogram_visualization_button.pack()


def draw_lines():
    for line_number in range(LINES_COUNT + 1):
        canvas_nonogram.create_line(
            0, line_number * 200/LINES_COUNT, 200, line_number * 200/LINES_COUNT)
    for column_number in range(COLUMNS_COUNT + 1):
        canvas_nonogram.create_line(
            column_number * 200/COLUMNS_COUNT, 0, column_number * 200/COLUMNS_COUNT, 200)


root.mainloop()
