'''

'''

import time
from logic.recipe_manager import RecipeManager


class MixerController:
    def __init__(self, pump_controller):
        self.recipe_manager = RecipeManager()
        self.pump_controller = pump_controller
        self.target_volume_ml = 200

    def mix(self, recipe_name):
        recipe = self.recipe_manager.get_recipe(recipe_name)
        if not recipe:
            print(f"Rezept '{recipe_name}' nicht gefunden.")
            return

        print(f"Starte Mischung: {recipe_name}")
        for ingredient, ratio in recipe.items():
            amount = self.target_volume_ml * ratio
            self.pump_controller.dispense(ingredient, amount)