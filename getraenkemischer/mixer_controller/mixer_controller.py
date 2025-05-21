class MixerController:
    def __init__(self):
        # Fiktive Rezepte (Pumpennummer: Laufzeit in Sekunden)
        self.recipes = {
            "Cola-Rum": {1: 2, 2: 2},
            "Saftschorle": {3: 3, 4: 1},
            "Eistee-Mix": {2: 2, 4: 2}
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
