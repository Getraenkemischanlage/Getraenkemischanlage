import tkinter as tk
from tkinter import ttk
from collections import Counter
import json
import os
import serial
import time

from recipe_manager import RecipeManager
from drink_suggestion import DrinkSuggestion
from sensor_manager import SensorManager


class BeverageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Getränkesteuerung")

        # Initialisiere SensorManager und lade erste Sensordaten
        self.sensor_manager = SensorManager()
        self.fill_levels = self.sensor_manager.read_fill_levels()
        self.logic = DrinkSuggestion(self.fill_levels.copy())

        self.bewertungen = []
        self.lade_bewertungen()

        self.letztes_getraenk = None

        self.text_output = tk.Text(root, height=6, width=50)
        self.text_output.pack(padx=10, pady=10)

        self.progress_bars = {}
        self.create_progress_bars()

        self.buttons = {}
        self.create_drink_buttons()

        self.suggest_button = tk.Button(root, text="Bestes Getränk vorschlagen", command=self.suggest_best)
        self.suggest_button.pack(pady=10)

        like_frame = tk.Frame(root)
        like_frame.pack()
        self.like_button = tk.Button(like_frame, text="Like", command=self.like_drink)
        self.like_button.pack(side=tk.LEFT, padx=10)

        self.dislike_button = tk.Button(like_frame, text="Dislike", command=self.dislike_drink)
        self.dislike_button.pack(side=tk.LEFT, padx=10)

        tk.Button(root, text="Top Getränke anzeigen", command=self.zeige_top_getraenke).pack(pady=5)
        tk.Button(root, text="NOT-AUS", command=self.emergency_stop, bg="white", fg="red").pack(pady=10)
        tk.Button(root, text="NOT-AUS zurücksetzen", command=self.reset_emergency_stop, bg="white", fg="green").pack(pady=5)

        # Schaltfläche zum manuellen Aktualisieren der Füllstände
        tk.Button(
            root, 
            text="Füllstände aktualisieren",
            command=self.request_sensor_data,
            bg="lightblue",
            width=20
        ).pack(pady=5)

        # Initialize serial connection
        self.serial_port = None
        try:
            self.serial_port = serial.Serial("COM5", baudrate=9600, timeout=1)
            if self.serial_port.is_open:
                print("Serielle Verbindung über SensorManager hergestellt")
            else:
                print("Keine Verbindung über SensorManager verfügbar")
        except Exception as e:
            print(f"Error accessing serial port: {e}")

    def create_progress_bars(self):
        tk.Label(self.root, text="Füllstände:").pack()
        for ingredient in ["Wasser", "Sirup_a", "Sirup_b", "Sirup_c"]:
            frame = tk.Frame(self.root)
            frame.pack(padx=10, pady=2, fill='x')
            tk.Label(frame, text=ingredient, width=10, anchor='w').pack(side='left')
            bar = ttk.Progressbar(frame, length=200, maximum=1000)
            bar.pack(side='left', fill='x')
            self.progress_bars[ingredient] = bar

    def create_drink_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        row = 0
        col = 0
        for i, drink in enumerate(self.logic.recipe_manager.get_all_recipes().keys()):
            btn = tk.Button(button_frame, text=drink, width=20,
                            command=lambda d=drink: self.mix_drink(d))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons[drink] = btn

            col += 1
            if col > 1:
                col = 0
                row += 1

    def update_progress_bars(self):
        # Sensor offsets
        self.OFFSETS = {
            "Wasser": 8070893,
            "Sirup_a": 8569537,
            "Sirup_b": 7868091,
            "Sirup_c": 8605134
        }
        
        for ingredient, bar in self.progress_bars.items():
            raw_value = self.fill_levels.get(ingredient, 0)
            # Apply offset calibration
            calibrated_value = raw_value - self.OFFSETS[ingredient]
            if calibrated_value < 0:
                calibrated_value = 1
                
            # Normalize for progress bar (0-1000)
            min_sensor_value = 0       # Empty container
            max_sensor_value = 1000000  # Full container
            normalized_value = max(0, min(1000, (calibrated_value / max_sensor_value) * 1000))
            bar['value'] = normalized_value

    def update_button_states(self):
        for drink, button in self.buttons.items():
            volume = self.logic.max_mixable_volume_ml(self.logic.recipe_manager.get_recipe(drink))
            button.config(state="normal" if volume >= self.logic.target_volume_ml else "disabled")

    def request_sensor_data(self):
        """Request sensor data only when needed"""
        try:
            self.fill_levels = self.sensor_manager.read_fill_levels()
            if self.fill_levels:
                self.logic.fill_levels = self.fill_levels.copy()
                self.update_progress_bars()
                self.update_button_states()
                
                # Update text display
                self.text_output.delete("1.0", tk.END)
                self.text_output.insert(tk.END, "Aktuelle Füllstände:\n")
                for ingredient, value in self.fill_levels.items():
                    raw_value = value
                    calibrated = raw_value - self.OFFSETS[ingredient]
                    if calibrated < 0:
                        calibrated = 1
                    percentage = min(100, max(0, (calibrated / 950000) * 100))
                    self.text_output.insert(tk.END, f"{ingredient}: {percentage:.1f}%\n")
            else:
                self.text_output.delete("1.0", tk.END)
                self.text_output.insert(tk.END, "Keine Sensordaten verfügbar\n")
                
        except Exception as e:
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, f"Fehler beim Lesen der Sensoren: {e}\n")

    def mix_drink(self, drink_name):
        self.text_output.delete("1.0", tk.END)
        if drink_name in self.logic.recipe_manager.get_all_recipes():
            recipe = self.logic.recipe_manager.get_recipe(drink_name)
            try:
                if self.serial_port and self.serial_port.is_open:
                    # Convert recipe to JSON and send
                    json_command = json.dumps(recipe)
                    # Add command prefix to distinguish from sensor data
                    self.serial_port.write(f"MIX:{json_command}\n".encode())
                    self.text_output.insert(tk.END, f"Mixe {drink_name}...\n")
                    time.sleep(5)  # Wait for mixing
                    self.request_sensor_data()  # Update sensors after mixing
                else:
                    self.text_output.insert(tk.END, "Keine Verbindung zu den Pumpen!\n")
                    return
            except Exception as e:
                self.text_output.insert(tk.END, f"Fehler beim Senden: {e}\n")
                return

            self.letztes_getraenk = drink_name
            self.request_sensor_data()
        else:
            self.text_output.insert(tk.END, "Rezept nicht vorhanden.\n")

    def suggest_best(self):
        self.text_output.delete("1.0", tk.END)
        result = self.logic.suggest_best_drink()
        self.text_output.insert(tk.END, result)
        self.request_sensor_data()

    def emergency_stop(self):
        for button in self.buttons.values():
            button.config(state="disabled")
        self.suggest_button.config(state="disabled")
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, "NOT-AUS aktiviert. Alle Pumpen gestoppt.\n")

    def reset_emergency_stop(self):
        self.update_button_states()
        self.suggest_button.config(state="normal")
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, "NOT-AUS zurückgesetzt. System wieder aktiv.\n")

    def lade_bewertungen(self, dateiname="bewertungen.json"):
        if os.path.exists(dateiname) and os.path.getsize(dateiname) > 0:
            with open(dateiname, "r") as f:
                self.bewertungen = json.load(f)
        else:
            self.bewertungen = []

    def speichere_bewertungen(self, dateiname="bewertungen.json"):
        try:
            with open(dateiname, "w") as f:
                json.dump(self.bewertungen, f, indent=2)
        except Exception as e:
            self.text_output.insert(tk.END, f"Fehler beim Speichern: {e}\n")

    def like_drink(self):
        if self.letztes_getraenk:
            self.bewertungen.append({"getränk": self.letztes_getraenk, "bewertung": "like"})
            self.text_output.insert(tk.END, f" '{self.letztes_getraenk}' wurde mit LIKE bewertet.\n")
            self.speichere_bewertungen()
        else:
            self.text_output.insert(tk.END, " Kein Getränk zum Bewerten ausgewählt.\n")

    def dislike_drink(self):
        if self.letztes_getraenk:
            self.bewertungen.append({"getränk": self.letztes_getraenk, "bewertung": "dislike"})
            self.text_output.insert(tk.END, f" '{self.letztes_getraenk}' wurde mit DISLIKE bewertet.\n")
            self.speichere_bewertungen()
        else:
            self.text_output.insert(tk.END, " Kein Getränk zum Bewerten ausgewählt.\n")

    def zeige_top_getraenke(self):
        self.text_output.insert(tk.END, "\n Meistgelikte Getränke:\n")
        likes = [b["getränk"] for b in self.bewertungen if b["bewertung"] == "like"]
        counter = Counter(likes)
        alle_getraenke = list({b["getränk"] for b in self.bewertungen})
        sortiert = sorted(alle_getraenke, key=lambda g: -counter.get(g, 0))
        for getraenk in sortiert:
            anzahl = counter.get(getraenk, 0)
            self.text_output.insert(tk.END, f"{getraenk}: {anzahl} Like(s)\n")
        if not self.bewertungen:
            self.text_output.insert(tk.END, "Noch keine Bewertungen vorhanden.\n")


# --- Programmstart ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BeverageGUI(root)
    root.mainloop()
