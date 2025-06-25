import tkinter as tk
from tkinter import ttk
from drink_suggestion import DrinkSuggestion
import json
import os
from collections import Counter
from recipe_manager import RecipeManager


# --- Dummy SensorManager Klasse ---
class SensorManager:            #Simuliert die aktuellen Füllstände der verschiedenen Zutaten
    def __init__(self):
        self.levels = {
            "Wasser": 800,
            "Sirup_a": 500,
            "Sirup_b": 400,
            "Alkohol": 300
        }

    def read_fill_levels(self):         #gibt Kopie der Füllstände zurück
        return self.levels.copy()


# --- Dummy BeverageSuggestion Klasse ---
class DrinkSuggestion:
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
        output = f"Getränk '{drink_name}' wird gemischt:\n"
        for ingredient, amount in self.recipes[drink_name].items():
            if self.fill_levels[ingredient] >= amount:
                self.fill_levels[ingredient] -= amount
                output += f" - {amount} ml {ingredient}\n"
            else:
                output += f" - Nicht genug {ingredient} verfügbar! ({self.fill_levels[ingredient]} ml vorhanden, {amount} ml benötigt)\n"
        return output

    def max_mixable_volume_ml(self, recipe):
        # Wie viele Portionen möglich?
        portions = [
        self.fill_levels.get(ing, 0) / amount
        for ing, amount in recipe.items()
        if amount > 0
        ]
        if not portions:
            return 0
        # Volumen pro Portion 
        portion_volume = sum(recipe.values())
        max_volume = min(portions) * portion_volume
        return int(max_volume)

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
        self.logic = DrinkSuggestion(self.fill_levels.copy())

        # Bewertung speichern
        self.bewertungen = []             
        self.lade_bewertungen()

        # Zuletzt gemixtes Getränk
        self.letztes_getraenk = None      

        self.text_output = tk.Text(root, height=6, width=50)
        self.text_output.pack(padx=10, pady=10)

        self.progress_bars = {}
        self.create_progress_bars()

        self.buttons = {}
        self.create_drink_buttons()

        self.suggest_button = tk.Button(root, text="Bestes Getränk vorschlagen", command=self.suggest_best)
        self.suggest_button.pack(pady=10)
        #Like/Dislike Buttons
        self.like_button = tk.Button(root, text="Like", command=self.like_drink)
        self.like_button.pack(pady=2)

        self.dislike_button = tk.Button(root, text="Dislike", command=self.dislike_drink)
        self.dislike_button.pack(pady=2)

        tk.Button(root, text="Top Getränke anzeigen", command=self.zeige_top_getraenke).pack(pady=5) #zeigt getränk mit meisten likes

        tk.Button(root, text="NOT-AUS", command=self.emergency_stop, bg="white", fg="red").pack(pady=10)
        tk.Button(root, text="NOT-AUS zurücksetzen", command=self.reset_emergency_stop, bg="white", fg="green").pack(pady=5)

        self.update_gui()

    def create_progress_bars(self):     #Erstellt die Fortschrittsbalken für die Füllstände
        tk.Label(self.root, text="Füllstände:").pack()
        for ingredient in ["Wasser", "Sirup_a", "Sirup_b", "Alkohol"]:
            frame = tk.Frame(self.root)
            frame.pack(padx=10, pady=2, fill='x')
            tk.Label(frame, text=ingredient, width=10, anchor='w').pack(side='left')
            bar = ttk.Progressbar(frame, length=200, maximum=1000)
            bar.pack(side='left', fill='x')
            self.progress_bars[ingredient] = bar

    def create_drink_buttons(self):     #Erstellt die Buttons für die Getränke
        for drink in self.logic.recipes.keys():
            btn = tk.Button(self.root, text=drink, width=25,
                            command=lambda d=drink: self.mix_drink(d))
            btn.pack(pady=2)
            self.buttons[drink] = btn

    def update_progress_bars(self):     #Aktualisiert die Fortschrittsbalken mit den aktuellen Füllständen
        for ingredient, bar in self.progress_bars.items():
            bar['value'] = self.fill_levels.get(ingredient, 0)

    def update_button_states(self):     #Aktualisiert die Zustände der Getränkebuttons basierend auf den Füllständen
        for drink, button in self.buttons.items():
            volume = self.logic.max_mixable_volume_ml(self.logic.recipes[drink])
            button.config(state="normal" if volume >= self.logic.target_volume_ml else "disabled")

    def update_gui(self):       #Aktualisiert die GUI mit den aktuellen Füllständen und Rezepten
        self.fill_levels = self.sensor_manager.read_fill_levels()
        self.logic = DrinkSuggestion(self.fill_levels.copy())
        self.update_progress_bars()
        self.update_button_states()

    def mix_drink(self, drink_name):
        self.text_output.delete("1.0", tk.END)

        if drink_name in self.logic.recipes:
            result = self.logic.apply_recipe(drink_name)
            self.letztes_getraenk = drink_name  # speichern

            if result:
                self.text_output.insert(tk.END, str(result))
            else:
                self.text_output.insert(tk.END, f"'{drink_name}' wurde gemixt.\n")

            self.update_gui()
        else:
            self.text_output.insert(tk.END, "Rezept nicht vorhanden.\n")

    def suggest_best(self):     #Schlägt das beste Getränk vor und aktualisiert die GUI
        self.text_output.delete("1.0", tk.END)
        result = self.logic.suggest_best_drink()
        self.text_output.insert(tk.END, result)
        self.update_gui()

    def emergency_stop(self):       #Aktiviert den NOT-AUS und stoppt alle Pumpen
    #Alle Getränkeknöpfe deaktivieren
        for button in self.buttons.values():
            button.config(state="disabled")

    #Getränk vorschlagen deaktivieren
        self.suggest_button.config(state="disabled")

    #Textausgabe aktualisieren
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, "NOT-AUS aktiviert. Alle Pumpen gestoppt.\n")
    
    def reset_emergency_stop(self):     #Setzt den NOT-AUS zurück und aktiviert die Pumpen wieder
        self.update_button_states()
        self.suggest_button.config(state="normal")
        self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, "NOT-AUS zurückgesetzt. System wieder aktiv.\n")

    def lade_bewertungen(self,dateiname="bewertungen.json"):
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



