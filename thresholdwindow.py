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

    def show(self):
        self.pack_widgets()
        self.root.mainloop()

    def set_threshold(self, threshold: int):
        self.threshold_label.configure(
            text=f"Tentative de résolution avec le seuil {threshold}")

    def set_time(self, time_in_seconds: int):
        if time_in_seconds < 120:
            self.time_label.configure(
                text="Temps restant : environ {time_in_seconds} secondes")
        else:
            time_in_minutes = (time_in_seconds + 30) // 60
            self.time_label.configure(
                text="Temps restant : environ {time_in_minutes} minutes")
