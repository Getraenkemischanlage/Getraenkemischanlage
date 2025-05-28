'''
import tkinter as tk
from tkinter import ttk

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Getränkemischanlage")

        # Getränkewahl
        self.drink_label = ttk.Label(root, text="Getränk auswählen:")
        self.drink_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.drink_selection = ttk.Combobox(root, values=["Cola-Rum", "Saftschorle", "Eistee-Mix"])
        self.drink_selection.grid(row=0, column=1, padx=10, pady=5)

        # Start/Stop Buttons
        self.start_button = ttk.Button(root, text="Mischen starten", command=self.start_mixing)
        self.start_button.grid(row=1, column=0, padx=10, pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_mixing)
        self.stop_button.grid(row=1, column=1, padx=10, pady=5)

        # Statusanzeige
        self.status_label = ttk.Label(root, text="Status:")
        self.status_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.status_display = tk.Text(root, height=5, width=40, state="disabled")
        self.status_display.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Sensoranzeige
        self.sensor_frame = ttk.LabelFrame(root, text="Sensorwerte")
        self.sensor_frame.grid(row=0, column=2, rowspan=4, padx=10, pady=5)

        self.temp_label = ttk.Label(self.sensor_frame, text="Temperatur: -- °C")
        self.temp_label.pack(anchor="w", padx=10, pady=5)

        self.fill_label = ttk.Label(self.sensor_frame, text="Füllstand: -- %")
        self.fill_label.pack(anchor="w", padx=10, pady=5)

    def start_mixing(self):
        self.update_status("Mischen gestartet...")

    def stop_mixing(self):
        self.update_status("Mischen gestoppt.")

    def update_status(self, message):
        self.status_display.configure(state="normal")
        self.status_display.insert("end", message + "\n")
        self.status_display.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
'''