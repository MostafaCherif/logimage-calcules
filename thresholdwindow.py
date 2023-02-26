import tkinter as tk


class ThresholdWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.threshold_label = tk.Label(
            text="Tentative de résolution avec le seuil .")
        self.time_label = tk.Label(text="Temps restant : environ . secondes")

    def pack_widgets(self):
        self.threshold_label.pack()
        self.time_label.pack()
        pass

    def show(self):
        self.pack_widgets()
        self.root.mainloop()
