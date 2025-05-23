import tkinter as tk
from tkinter import ttk
from controller.mixer_controller import MixerController

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Getränkemischanlage")

        # Controller-Instanz
        self.mixer = MixerController()

        # GUI-Elemente
        self.drink_label = ttk.Label(root, text="Getränk auswählen:")
        self.drink_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.drink_selection = ttk.Combobox(root, values=list(self.mixer.recipes.keys()))
        self.drink_selection.grid(row=0, column=1, padx=10, pady=5)

        self.start_button = ttk.Button(root, text="Mischen starten", command=self.start_mixing)
        self.start_button.grid(row=1, column=0, padx=10, pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_mixing)
        self.stop_button.grid(row=1, column=1, padx=10, pady=5)

        self.status_display = tk.Text(root, height=6, width=50, state="disabled")
        self.status_display.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def start_mixing(self):
        drink = self.drink_selection.get()
        if not drink:
            self.update_status("⚠ Bitte ein Getränk auswählen!")
            return
        self.update_status(f"Starte Mischung: {drink}")
        self.mixer.mix(drink)
        self.update_status(f"Mischung {drink} abgeschlossen.")

    def stop_mixing(self):
        self.update_status("Mischung gestoppt (funktional noch nicht implementiert)")

    def update_status(self, message):
        self.status_display.configure(state="normal")
        self.status_display.insert("end", message + "\n")
        self.status_display.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
