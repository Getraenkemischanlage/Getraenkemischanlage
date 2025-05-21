class MixerController:
    def __init__(self):
        # Fiktive Rezepte (Pumpennummer: Laufzeit in Sekunden)
        self.recipes = {
            "Cola-Mix":         {"Wasser": 0.3, "Sirup_a": 0.7,},
            "Cocktail":         {"Alkohol": 0.4, "Sirup_b": 0.2, "Wasser": 0.4},
            "Schorle":          {"Wasser": 0.5, "Sirup_b": 0.5},
            "Cola-Light Mix":   {"Wasser": 0.7, "Sirup_a": 0.3}
        }

    def mix(self, recipe_name):
        if recipe_name not in self.recipes:
            print(f"Rezept '{recipe_name}' nicht gefunden.")
            return

        recipe = self.recipes[recipe_name]
        for pump_id, duration in recipe.items():
            self.activate_pump(pump_id, duration)

    def activate_pump(self, pump_id, duration):
        print(f"Pumpe {pump_id} für {duration} Sekunden aktiv.")
        # Hier käme die GPIO-Steuerung mit z. B. time.sleep().
