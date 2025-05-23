import time
from ..hardware.pump_controller import PumpController  # Stelle sicher, dass diese Datei existiert

class MixerController:
    def __init__(self, pump_controller=None):
        """
        Initialisiert den MixerController mit optional übergebenem PumpController.
        """
        self.pump_controller = pump_controller or PumpController()

        # Rezepte mit Pumpennamen und Laufzeit in Sekunden
        self.recipes = {
            "Cola-Mix":         {"water": 0.3, "syrup_a": 0.7},
            "Cocktail":         {"alcohol": 0.4, "syrup_b": 0.2, "water": 0.4},
            "Schorle":          {"water": 0.5, "syrup_b": 0.5},
            "Cola-Light Mix":   {"water": 0.7, "syrup_a": 0.3}
        }

    def mix(self, recipe_name):
        """
        Führt das Rezept aus, indem die entsprechenden Pumpen aktiviert werden.
        """
        if recipe_name not in self.recipes:
            print(f"Rezept '{recipe_name}' nicht gefunden.")
            return

        print(f"\nStarte Mischung: {recipe_name}")
        recipe = self.recipes[recipe_name]

        for ingredient, duration in recipe.items():
            self.activate_pump(ingredient, duration)

        print("Mischung abgeschlossen.\n")

    def activate_pump(self, ingredient, duration):
        """
        Aktiviert eine bestimmte Pumpe für die angegebene Dauer.
        """
        print(f"Aktiviere Pumpe für '{ingredient}' für {duration:.2f} Sekunden.")
        if self.pump_controller and ingredient in self.pump_controller.pumps:
            pump = self.pump_controller.pumps[ingredient]
            if pump:
                pump.value(1)
                time.sleep(duration)
                pump.value(0)
            else:
                # Simulationsmodus
                time.sleep(duration)
        else:
            print(f"WARNUNG: Keine Pumpe für '{ingredient}' definiert.")
