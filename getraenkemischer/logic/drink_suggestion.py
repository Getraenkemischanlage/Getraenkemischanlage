'''
Klassen:
- DrinkSuggestion
    Klassenobjekte:
    - fill_levels: dict
    - target_volume_ml: int
    - recipe_manager: RecipeManager
    Klassenmethoden:
    - __init__(fill_levels: dict)
    - suggest_best_drink(): None
    - max_mixable_volume_ml(recipe: dict)   (gibt float zurürck)
    - apply_recipe(recipe_name: str): None
'''

from hardware.sensor_manager import SensorManager
from recipe_manager import RecipeManager

class DrinkSuggestion:
    def __init__(self, fill_levels):
        
        self.fill_levels = fill_levels  # Füllstände 

        self.target_volume_ml = 200 # Zielmenge in ml

        self.recipe_manager = RecipeManager()   # holt Rezepte
        
     
    def suggest_best_drink(self):
        best_drink = None
        max_possible_volume = 0

        for name, ingredients in self.recipe_manager.get_all_recipes().items():
            volume = self.max_mixable_volume_ml(ingredients)
            if volume >= self.target_volume_ml and volume > max_possible_volume:
                best_drink = name
                max_possible_volume = volume

        if best_drink:
            print(f"Empfohlenes Getränk: {best_drink} (max. {int(max_possible_volume)} ml mischbar)")
            self.apply_recipe(best_drink)
            print("\nAktueller Füllstand nach Mischung:")
            for k, v in self.fill_levels.items():
                print(f"  {k}: {int(v)} ml")
        else:
            print("Kein Getränk mischbar mit aktuellem Füllstand.")

    def max_mixable_volume_ml(self, recipe):
        max_volume = float('inf')
        for ingredient, fraction in recipe.items():
            available = self.fill_levels.get(ingredient, 0)
            if fraction > 0:
                possible_volume = available / fraction
                max_volume = min(max_volume, possible_volume)
        return max_volume

    def apply_recipe(self, recipe_name):
        recipe = self.recipe_manager.get_recipe(recipe_name)
        print(f"\nMische {self.target_volume_ml} ml {recipe_name}...")
        for ingredient, fraction in recipe.items():
            needed = self.target_volume_ml * fraction
            self.fill_levels[ingredient] -= needed

sensor_manager = SensorManager()
current_fill_levels = sensor_manager.read_sensors()

suggestion = DrinkSuggestion(current_fill_levels)
suggestion.suggest_best_drink()
