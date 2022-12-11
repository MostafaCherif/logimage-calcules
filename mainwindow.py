import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from board import Board
from nonogram import board_to_nonogram
import numpy as np
from images_processing import grayscale_img, resize_img, to_board
from nonogramwindow import create_window
import generateur
import generateur_edgy

imPath = "test"

LINES_COUNT = 3
COLUMNS_COUNT = 3
IMAGE_HEIGHT = 200
IMAGE_WIDTH = 800


root = tk.Tk()

insert_label = tk.Label(text="Ajoutez votre image ici")
insert_label.pack(anchor="w")

image = tk.Label(anchor="w")
nonogram = None


def load_image_button_pressed():
    openImageFile()


def validation_button_pressed():
    global imPath, canvas_nonogram, LINES_COUNT, COLUMNS_COUNT, nonogram
    LINES_COUNT = int(entry_horizontal.get())
    COLUMNS_COUNT = int(entry_vertical.get())
    board = board_from_image(imPath)
    nonogram = board_to_nonogram(board)
    draw_board_in_canvas(canvas_nonogram, board)


def nonogram_visualization_button_pressed():
    global nonogram
    create_window(nonogram)


def unicity_button_pressed():
    global nonogram
    global canvas_nonogram
    if nonogram is None:
        tk.messagebox.showerror("Logimage manquant",
                                "Aucun logimage à analyser !")
        return

    try:
        one_solution = nonogram.solve()
        if one_solution:
            messagebox.showinfo("Analyse de logimage",
                                "Le logimage admet bien une unique solution !")
        else:
            messagebox.showwarning(
                "Analyse de logimage", "Le logimage admet plusieurs solutions :(")
    except Exception as e:
        if "timeout" in str(e):
            messagebox.showwarning(
                "Analyse de logimage", "Le logimage admet plusieurs solutions ou alors l'analyse prend du temps :(")


def openImageFile():
    global img, image, imPath, IMAGE_HEIGHT, IMAGE_WIDTH
    imPath = filedialog.askopenfilename(initialdir=".", title="Open an image", filetypes=(
        ("Image file", "*.png"), ("Image file", "*.jpeg"), ("Image file", "*.jpg"), ("All File Types", "*.*")))
    if imPath:
        PILimg = Image.open(imPath)
        PILimg = resize_img(PILimg, 200)
        img = ImageTk.PhotoImage(PILimg)
        IMAGE_WIDTH, IMAGE_HEIGHT = PILimg.size
        image.configure(image=img)


def draw_board_in_canvas(canvas: tk.Canvas, board: Board) -> None:
    global IMAGE_HEIGHT, IMAGE_WIDTH
    canvas.delete("all")
    data = board.data
    lines_count, columns_count = board.width, board.height
    for j, i in np.ndindex(data.shape):
        if data[j, i] == 1:
            canvas.create_rectangle(
                i * IMAGE_WIDTH/lines_count,
                j * IMAGE_HEIGHT/columns_count,
                (i + 1) * IMAGE_WIDTH/lines_count,
                (j + 1) * IMAGE_HEIGHT/columns_count,
                fill="#000")
        else:
            canvas.create_rectangle(
                i * IMAGE_WIDTH/lines_count,
                j * IMAGE_HEIGHT/columns_count,
                (i + 1) * IMAGE_WIDTH/lines_count,
                (j + 1) * IMAGE_HEIGHT/columns_count,
                fill="#fff")


def board_from_image(path: str):
    global slider, LINES_COUNT, COLUMNS_COUNT, selectedChoice
    preprocessed_img = None
    if selectedChoice.get() == "NoEdgy":
        preprocessed_img = generateur.preprocess_image(
            path, threshold=slider.get(), output_size=(COLUMNS_COUNT, LINES_COUNT))
    elif selectedChoice.get() == "Edgy":
        preprocessed_img = generateur_edgy.preprocess_image(
            path, threshold=slider.get(), output_size=(COLUMNS_COUNT, LINES_COUNT))
    return Board(data=preprocessed_img)


load_image_button = tk.Button(
    text="Choisissez une image...", command=load_image_button_pressed)
load_image_button.pack(anchor="w")

image.pack(anchor="w")

label_entry_horizontal = tk.Label(
    text="Entrez le nombre de lignes du logimage")
entry_horizontal = tk.Entry(root)
entry_horizontal.insert(0, "5")
label_entry_vertical = tk.Label(
    text="Entrez le nombre de colonnes du logimage")
entry_vertical = tk.Entry(root)
entry_vertical.insert(0, "5")

label_entry_horizontal.pack(anchor="w")
entry_horizontal.pack(anchor="w")
label_entry_vertical.pack(anchor="w")
entry_vertical.pack(anchor="w")


slider = tk.Scale(from_=0, to=255, tickinterval=32,
                  length=250, orient="horizontal")
slider.pack(anchor="w")

selectedChoice = tk.StringVar()
rbNoEdgy = tk.Radiobutton(root, text="Image complète",
                          variable=selectedChoice, value="NoEdgy")
rbEdgy = tk.Radiobutton(root, text="Contours uniquement",
                        variable=selectedChoice, value="Edgy")
rbNoEdgy.pack(anchor="w")
rbEdgy.pack(anchor="w")

validation_button = tk.Button(
    text="Valider", command=validation_button_pressed)
validation_button.pack(anchor="w")

canvas_nonogram = tk.Canvas(width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
canvas_nonogram.pack(anchor="w")

check_for_unicity_button = tk.Button(
    text="Vérifier l'existence et l'unicité d'une solution", command=unicity_button_pressed
)

check_for_unicity_button.pack(anchor="w")
nonogram_visualization_button = tk.Button(
    text="Visualiser le logimage vide", command=nonogram_visualization_button_pressed
)
nonogram_visualization_button.pack(anchor="w")


root.mainloop()
