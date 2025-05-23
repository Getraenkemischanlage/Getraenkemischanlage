import tkinter as tk
from tkinter import ttk

# --- Dummy SensorManager Klasse ---
class SensorManager:
    def __init__(self):
        self.levels = {
            "Wasser": 800,
            "Sirup_a": 500,
            "Sirup_b": 400,
            "Alkohol": 300
        }

    def read_fill_levels(self):
        return self.levels.copy()

# --- Dummy BeverageSuggestion Klasse ---
class BeverageSuggestion:
    def __init__(self, fill_levels):
        self.fill_levels = fill_levels
        self.target_volume_ml = 200
        self.recipes = {
             "Cola-Mix":         {"Wasser": 60, "Sirup_a": 140,},
            "Cocktail":         {"Alkohol": 80, "Sirup_b": 40, "Wasser": 80},
            "Schorle":          {"Wasser": 100, "Sirup_b": 100},
            "Cola-Light Mix":   {"Wasser": 140, "Sirup_a": 60}
        }

    def apply_recipe(self, drink_name):
        for ingredient, amount in self.recipes[drink_name].items():
            if self.fill_levels[ingredient] >= amount:
                self.fill_levels[ingredient] -= amount

    def max_mixable_volume_ml(self, recipe):
        volumes = [
            self.fill_levels.get(ing, 0) // amount
            for ing, amount in recipe.items()
        ]
        return min(volumes) * sum(recipe.values()) if volumes else 0

    def suggest_best_drink(self):
        best = None
        max_vol = 0
        for name, recipe in self.recipes.items():
            vol = self.max_mixable_volume_ml(recipe)
            if vol >= self.target_volume_ml and vol > max_vol:
                max_vol = vol
                best = name
        return f"Empfohlenes Getränk: {best} ({max_vol} ml)\n" if best else "Kein geeignetes Getränk gefunden.\n"

# --- GUI Klasse ---
class BeverageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Getränkesteuerung")

        self.sensor_manager = SensorManager()
        self.fill_levels = self.sensor_manager.read_fill_levels()
        self.logic = BeverageSuggestion(self.fill_levels.copy())

        self.text_output = tk.Text(root, height=6, width=50)
        self.text_output.pack(padx=10, pady=10)

        self.progress_bars = {}
        self.create_progress_bars()

        self.buttons = {}
        self.create_drink_buttons()

        tk.Button(root, text="Bestes Getränk vorschlagen", command=self.suggest_best).pack(pady=10)

        self.update_gui()

    def create_progress_bars(self):
        tk.Label(self.root, text="Füllstände:").pack()
        for ingredient in ["Wasser", "Sirup_a", "Sirup_b", "Alkohol"]:
            frame = tk.Frame(self.root)
            frame.pack(padx=10, pady=2, fill='x')
            tk.Label(frame, text=ingredient, width=10, anchor='w').pack(side='left')
            bar = ttk.Progressbar(frame, length=200, maximum=1000)
            bar.pack(side='left', fill='x')
            self.progress_bars[ingredient] = bar

    def create_drink_buttons(self):
        for drink in self.logic.recipes.keys():
            btn = tk.Button(self.root, text=drink, width=25,
                            command=lambda d=drink: self.mix_drink(d))
            btn.pack(pady=2)
            self.buttons[drink] = btn

    def update_progress_bars(self):
        for ingredient, bar in self.progress_bars.items():
            bar['value'] = self.fill_levels.get(ingredient, 0)

    def update_button_states(self):
        for drink, button in self.buttons.items():
            volume = self.logic.max_mixable_volume_ml(self.logic.recipes[drink])
            button.config(state="normal" if volume >= self.logic.target_volume_ml else "disabled")

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
            self.text_output.insert(tk.END, "Rezept nicht vorhanden.\n")
        self.update_gui()

    def suggest_best(self):
        self.text_output.delete("1.0", tk.END)
        result = self.logic.suggest_best_drink()
        self.text_output.insert(tk.END, result)
        self.update_gui()

# --- Programmstart ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BeverageGUI(root)
    root.mainloop()