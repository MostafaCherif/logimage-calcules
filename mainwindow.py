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


class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.lines_count = 3
        self.columns_count = 3
        self.imPath = "test"
        self.insert_label = tk.Label(text="Ajoutez votre image ici")
        self.label_image = tk.Label()
        self.nonogram = None
        self.load_image_button = tk.Button(
            text="Choisissez une image...",
            command=self.load_image_button_pressed)
        self.label_entry_horizontal = tk.Label(
            text="Entrez le nombre de lignes du logimage")
        self.entry_horizontal = tk.Entry(self.root)
        self.entry_horizontal.insert(0, "5")
        self.label_entry_vertical = tk.Label(
            text="Entrez le nombre de colonnes du logimage")
        self.entry_vertical = tk.Entry(self.root)
        self.entry_vertical.insert(0, "5")
        self.slider = tk.Scale(
            from_=0,
            to=255,
            tickinterval=32,
            length=250,
            orient="horizontal")
        self.selectedChoice = tk.StringVar(None, value=" ")
        self.rbNoEdgy = tk.Radiobutton(
            self.root, text="Image complète", variable=self.selectedChoice, value="NoEdgy")
        self.rbEdgy = tk.Radiobutton(
            self.root, text="Contours uniquement", variable=self.selectedChoice, value="Edgy")
        self.rbNoEdgy.pack(anchor="w")
        self.rbEdgy.pack(anchor="w")

        self.validation_button = tk.Button(
            text="Valider", command=self.validation_button_pressed)

        self.canvas_nonogram = tk.Canvas(width=202, height=202)

        self.check_for_unicity_button = tk.Button(
            text="Vérifier l'existence et l'unicité d'une solution", command=self.unicity_button_pressed
        )

        self.nonogram_visualization_button = tk.Button(
            text="Visualiser le logimage vide", command=self.nonogram_visualization_button_pressed
        )

    def pack_widgets(self):
        self.insert_label.pack()
        self.load_image_button.pack()
        self.label_image.pack()
        self.label_entry_horizontal.pack()
        self.entry_horizontal.pack()
        self.label_entry_vertical.pack()
        self.entry_vertical.pack()
        self.slider.pack()
        self.rbNoEdgy.pack()
        self.rbEdgy.pack()
        self.validation_button.pack()
        self.canvas_nonogram.pack()
        self.check_for_unicity_button.pack()
        self.nonogram_visualization_button.pack()

    def load_image_button_pressed(self):
        self.openImageFile()

    def validation_button_pressed(self):
        self.lines_count = int(self.entry_horizontal.get())
        self.columns_count = int(self.entry_vertical.get())
        board = self.board_from_image(self.imPath)
        self.nonogram = board_to_nonogram(board)
        self.draw_board_in_canvas(self.canvas_nonogram, board)

    def nonogram_visualization_button_pressed(self):
        create_window(self.nonogram)

    def unicity_button_pressed(self):
        if self.nonogram is None:
            tk.messagebox.showerror(
                "Logimage manquant", "Aucun logimage à analyser !")
            return

        try:
            one_solution = self.nonogram.solve()
            if one_solution:
                messagebox.showinfo(
                    "Analyse de logimage", "Le logimage admet bien une unique solution !")
            else:
                messagebox.showwarning(
                    "Analyse de logimage", "Le logimage admet plusieurs solutions :(")

        except Exception as e:
            if "timeout" in str(e):
                messagebox.showwarning(
                    "Analyse de logimage", "Le logimage admet plusieurs solutions ou alors l'analyse prend du temps :(")

    def openImageFile(self):
        self.imPath = filedialog.askopenfilename(initialdir=".", title="Open an image", filetypes=(
            ("Image file", "*.png"), ("Image file", "*.jpeg"), ("Image file", "*.jpg"), ("All File Types", "*.*")))
        if self.imPath:
            PILimg = Image.open(self.imPath)
            PILimg = PILimg.resize((200, 200))
            img = ImageTk.PhotoImage(PILimg)
            self.label_image.configure(image=img)
            self.label_image.image = img

    def draw_board_in_canvas(self, canvas: tk.Canvas, board: Board) -> None:
        self.draw_lines()
        data = board.data.T
        for i, j in np.ndindex(data.shape):
            if data[i, j] == 1:
                canvas.create_rectangle(
                    i * 200/self.lines_count, j * 200/self.columns_count, (i + 1) * 200/self.lines_count, (j + 1) * 200/self.columns_count, fill="#000")
            else:
                canvas.create_rectangle(
                    i * 200/self.lines_count, j * 200/self.columns_count, (i + 1) * 200/self.lines_count, (j + 1) * 200/self.columns_count, fill="#fff")

    def board_from_image(self, path: str):
        preprocessed_img = None
        if self.selectedChoice.get() == "NoEdgy":
            preprocessed_img = generateur.preprocess_image(
                path, threshold=self.slider.get(), output_size=(self.lines_count, self.columns_count))
        elif self.selectedChoice.get() == "Edgy":
            preprocessed_img = generateur_edgy.preprocess_image(
                path, threshold=self.slider.get(), output_size=(self.lines_count, self.columns_count))
        return Board(data=preprocessed_img)

    def draw_lines(self):
        for line_number in range(self.lines_count + 1):
            self.canvas_nonogram.create_line(
                0,
                line_number * 200/self.lines_count,
                200,
                line_number * 200/self.lines_count)

        for column_number in range(self.columns_count + 1):
            self.canvas_nonogram.create_line(
                column_number * 200/self.columns_count,
                0,
                column_number * 200/self.columns_count,
                200)

    def show(self):
        self.pack_widgets()
        self.root.mainloop()


"""imPath = "test"

LINES_COUNT = 3
COLUMNS_COUNT = 3


root = tk.Tk()

insert_label = tk.Label(text="Ajoutez votre image ici")
-insert_label.pack()

label_image = tk.Label()
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
        tk.messagebox.showerror("Logimage manquant", "Aucun logimage à analyser !")
        return
    
    try:
        one_solution = nonogram.solve()
    except Exception as e:
        if "timeout" in e:
            tk.messagebox.showwarning("Analyse de logimage", "Le logimage admet plusieurs solutions ou alors l'analyse prend du temps :(")
    if one_solution:
        tk.messagebox.showinfo("Analyse de logimage", "Le logimage admet bien une unique solution !")
    else:
        tk.messagebox.showwarning("Analyse de logimage", "Le logimage admet plusieurs solutions :(")


def openImageFile():
    global img, label_image, imPath
    imPath = filedialog.askopenfilename(initialdir=".", title="Open an image", filetypes=(
        ("Image file", "*.png"), ("Image file", "*.jpeg"), ("Image file", "*.jpg"), ("All File Types", "*.*")))
    if imPath:
        PILimg = Image.open(imPath)
        PILimg = PILimg.resize((200, 200))
        img = ImageTk.PhotoImage(PILimg)
        label_image.configure(image=img)


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
    global slider, LINES_COUNT, COLUMNS_COUNT, selectedChoice
    preprocessed_img = None
    if selectedChoice.get() == "NoEdgy":
        preprocessed_img = generateur.preprocess_image(path, threshold=slider.get(), output_size=(LINES_COUNT, COLUMNS_COUNT))
    elif selectedChoice.get() == "Edgy":
        preprocessed_img = generateur_edgy.preprocess_image(path, threshold=slider.get(), output_size=(LINES_COUNT, COLUMNS_COUNT))
    return Board(data=preprocessed_img)"""


"""load_image_button = tk.Button(
    text="Choisissez une image...", command=load_image_button_pressed)
-load_image_button.pack()

-label_image.pack()

label_entry_horizontal = tk.Label(
    text="Entrez le nombre de lignes du logimage")
entry_horizontal = tk.Entry(root)
entry_horizontal.insert(0, "5")
label_entry_vertical = tk.Label(
    text="Entrez le nombre de colonnes du logimage")
entry_vertical = tk.Entry(root)
entry_vertical.insert(0, "5")

-label_entry_horizontal.pack()
-entry_horizontal.pack()
-label_entry_vertical.pack()
-entry_vertical.pack()"""


"""slider = tk.Scale(from_=0, to=255, tickinterval=32,
                  length=250, orient="horizontal")
slider.pack()"""

"""selectedChoice = tk.StringVar()
rbNoEdgy = tk.Radiobutton(root, text="Image complète", variable=selectedChoice, value="NoEdgy")
rbEdgy = tk.Radiobutton(root, text="Contours uniquement", variable=selectedChoice, value="Edgy")
-rbNoEdgy.pack(anchor="w")
-rbEdgy.pack(anchor="w")

validation_button = tk.Button(
    text="Valider", command=validation_button_pressed)
-validation_button.pack()

canvas_nonogram = tk.Canvas(width=202, height=202)
-canvas_nonogram.pack()

check_for_unicity_button = tk.Button(
    text="Vérifier l'existence et l'unicité d'une solution", command=unicity_button_pressed
)

-check_for_unicity_button.pack()
nonogram_visualization_button = tk.Button(
    text="Visualiser le logimage vide", command=nonogram_visualization_button_pressed
)
-nonogram_visualization_button.pack()"""

"""
def draw_lines():
    for line_number in range(LINES_COUNT + 1):
        canvas_nonogram.create_line(
            0, line_number * 200/LINES_COUNT, 200, line_number * 200/LINES_COUNT)
    for column_number in range(COLUMNS_COUNT + 1):
        canvas_nonogram.create_line(
            column_number * 200/COLUMNS_COUNT, 0, column_number * 200/COLUMNS_COUNT, 200)"""


"""root.mainloop()"""
