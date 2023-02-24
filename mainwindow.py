import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from board import Board
from nonogram import board_to_nonogram
import numpy as np
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
            text="Entrez le nombre de lignes du logimage :")
        self.entry_lines = tk.Entry(self.root, width=2)
        self.entry_lines.insert(0, "5")
        self.label_entry_vertical = tk.Label(
            text="Entrez le nombre de colonnes du logimage :")
        self.entry_columns = tk.Entry(self.root, width=2)
        self.entry_columns.insert(0, "5")
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

        self.validation_button = tk.Button(
            text="Valider les paramètres du logimage", command=self.validation_button_pressed)

        self.canvas_nonogram = tk.Canvas(width=202, height=202)

        self.check_for_unicity_button = tk.Button(
            text="Vérifier l'existence et l'unicité d'une solution", command=self.unicity_button_pressed
        )

        self.nonogram_visualization_button = tk.Button(
            text="Visualiser le logimage vide", command=self.nonogram_visualization_button_pressed
        )

    def pack_widgets(self):
        self.insert_label.grid(row=0, column=0)
        self.load_image_button.grid(row=1, column=0)
        self.label_image.grid(row=2, column=0, rowspan=2, padx=3, pady=3)

        self.rbNoEdgy.grid(row=0, column=1, columnspan=2)
        self.rbEdgy.grid(row=0, column=3, columnspan=2)
        self.label_entry_horizontal.grid(row=1, column=1, sticky="E")
        self.entry_lines.grid(row=1, column=2, sticky="W")
        self.label_entry_vertical.grid(row=1, column=3, sticky="E")
        self.entry_columns.grid(row=1, column=4, sticky="W")
        self.slider.grid(row=2, column=1, columnspan=4)
        self.validation_button.grid(
            row=3, column=1, columnspan=4, ipadx=5, ipady=5)

        self.canvas_nonogram.grid(row=4, column=0, padx=3, pady=3)
        self.check_for_unicity_button.grid(row=5, column=0, columnspan=2)
        self.nonogram_visualization_button.grid(row=5, column=4)

        # Dynamic reshaping when extending the main window
        COLWEIGHTS = [1, 1, 0, 1, 0]
        ROW_MIN_SIZES = [25, 25, 50, 155, 205, 25]
        for col in range(5):
            self.root.columnconfigure(col, pad=8, weight=COLWEIGHTS[col])

        for row in range(6):
            self.root.rowconfigure(row, pad=8, weight=1,
                                   minsize=ROW_MIN_SIZES[row])

    def load_image_button_pressed(self):
        self.openImageFile()

    def validation_button_pressed(self):
        self.lines_count = int(self.entry_lines.get())
        self.columns_count = int(self.entry_columns.get())
        board = self.board_from_image(self.imPath)
        self.nonogram = board_to_nonogram(board)
        self.draw_board_in_canvas(self.canvas_nonogram, board)

    def nonogram_visualization_button_pressed(self):
        create_window(self.nonogram)

    def unicity_button_pressed(self):
        if self.nonogram is None:
            tk.messagebox.showerror(
                "Logimage manquant", "Aucun logimage à analyser !",
                parent=self.root)
            return

        try:
            one_solution = self.nonogram.solve()
            if one_solution:
                messagebox.showinfo(
                    "Analyse de logimage", "Le logimage admet bien une unique solution !",
                    parent=self.root)
            else:
                messagebox.showwarning(
                    "Analyse de logimage", "Le logimage admet plusieurs solutions :(",
                    parent=self.root)

        except Exception as e:
            if "timeout" in str(e):
                messagebox.showwarning(
                    "Analyse de logimage", "Le logimage admet plusieurs solutions ou alors l'analyse prend du temps :(",
                    parent=self.root)
            else:
                print("Exception:")
                print(e)

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
                    i * 200/self.columns_count, j * 200/self.lines_count, (i + 1) * 200/self.columns_count, (j + 1) * 200/self.lines_count, fill="#000")
            else:
                canvas.create_rectangle(
                    i * 200/self.columns_count, j * 200/self.lines_count, (i + 1) * 200/self.columns_count, (j + 1) * 200/self.lines_count, fill="#fff")

    def board_from_image(self, path: str, threshold: int=None):
        if threshold is None:
            threshold = self.slider.get()
        preprocessed_img = None
        if self.selectedChoice.get() == "NoEdgy":
            preprocessed_img = generateur.preprocess_image(
                path, threshold=threshold, output_size=(self.columns_count, self.lines_count))
        elif self.selectedChoice.get() == "Edgy":
            preprocessed_img = generateur_edgy.preprocess_image(
                path, threshold=threshold, output_size=(self.columns_count, self.lines_count))
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
