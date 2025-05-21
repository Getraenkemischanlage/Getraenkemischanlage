# gui.py
import tkinter as tk
from tkinter import ttk
from ..hardware.sensor_manager import SensorManager
from ..algorithmus.drink_suggestion import BeverageSuggestion

class BeverageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Getränkesteuerung")

        self.sensor_manager = SensorManager()
        self.fill_levels = self.sensor_manager.read_fill_levels()
        self.logic = BeverageSuggestion(self.fill_levels.copy())

        self.text_output = tk.Text(root, height=10, width=50)
        self.text_output.pack(padx=10, pady=10)

        self.progress_bars = {}
        self.create_progress_bars(root)

        self.buttons = {}
        self.drinks = list(self.logic.recipes.keys())
        for drink in self.drinks:
            btn = tk.Button(root, text=drink, width=25,
                            command=lambda d=drink: self.mix_drink(d))
            btn.pack(pady=2)
            self.buttons[drink] = btn

        tk.Button(root, text="Bestes Getränk vorschlagen",
                  command=self.suggest_best).pack(pady=10)

        self.update_gui()

    def create_progress_bars(self, parent):
        tk.Label(parent, text="Füllstände der Zutaten:").pack()
        for ingredient in ["Wasser", "Sirup_a", "Sirup_b", "Alkohol"]:
            frame = tk.Frame(parent)
            frame.pack(padx=10, pady=2, fill='x')
            tk.Label(frame, text=ingredient, width=12, anchor='w').pack(side='left')
            bar = ttk.Progressbar(frame, length=200, maximum=1000)
            bar.pack(side='left')
            self.progress_bars[ingredient] = bar

    def update_progress_bars(self):
        for ingredient, bar in self.progress_bars.items():
            ml = self.fill_levels.get(ingredient, 0)
            bar['value'] = ml

    def update_button_states(self):
        for drink, button in self.buttons.items():
            volume = self.logic.max_mixable_volume_ml(self.logic.recipes[drink])
            if volume >= self.logic.target_volume_ml:
                button.config(state="normal")
            else:
                button.config(state="disabled")

    def update_gui(self):
        self.fill_levels = self.sensor_manager.read_fill_levels()
        self.logic = BeverageSuggestion(self.fill_levels.copy())
        self.update_progress_bars()
        self.update_button_states()

    def mix_drink(self, drink_name):
        self.text_output.delete("1.0", tk.END)
        if drink_name in self.logic.recipes:
            self.logic.apply_recipe(drink_name)
            self.text_output.insert(tk.END, f"{drink_name} wurde gemischt ({self.logic.target_volume_ml} ml)\n")
        else:
            self.text_output.insert(tk.END, "Rezept nicht vorhanden.")
        self.update_gui()

    def suggest_best(self):
        self.text_output.delete("1.0", tk.END)
        import io, sys
        buffer = io.StringIO()
        sys.stdout = buffer
        self.logic.suggest_best_drink()
        sys.stdout = sys.__stdout__
        result = buffer.getvalue()
        self.text_output.insert(tk.END, result)
        self.update_gui()

# Start the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = BeverageGUI(root)
    root.mainloop()

