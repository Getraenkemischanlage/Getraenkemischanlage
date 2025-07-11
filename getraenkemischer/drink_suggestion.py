from sensor_manager import SensorManager
from recipe_manager import RecipeManager

class DrinkSuggestion:
    def __init__(self, fill_levels):
        self.fill_levels = fill_levels  # Aktuelle Füllstände
        self.target_volume_ml = 200     # Zielvolumen in ml
        self.recipe_manager = RecipeManager()

    def suggest_best_drink(self):
        best_drink = None
        max_possible_volume = 0

        for name, ingredients in self.recipe_manager.get_all_recipes().items():
            volume = self.max_mixable_volume_ml(ingredients)
            if volume >= self.target_volume_ml and volume > max_possible_volume:
                best_drink = name
                max_possible_volume = volume

        if best_drink:
            self.apply_recipe(best_drink)
            status = f"Empfohlenes Getränk: {best_drink} (max. {int(max_possible_volume)} ml mischbar)\n"
            status += "\nAktueller Füllstand nach Mischung:\n"
            for k, v in self.fill_levels.items():
                status += f"  {k}: {int(v)} ml\n"
            return status
        else:
            return "Kein Getränk mischbar mit aktuellem Füllstand.\n"

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
        if not recipe:
            return f"Rezept '{recipe_name}' nicht gefunden.\n"

        for ingredient, fraction in recipe.items():
            needed = self.target_volume_ml * fraction
            self.fill_levels[ingredient] -= needed

        return f"{recipe_name} wurde gemischt ({self.target_volume_ml} ml).\n"
