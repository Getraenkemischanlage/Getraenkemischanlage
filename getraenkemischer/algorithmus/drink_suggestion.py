class BeverageSuggestion:
    def __init__(self, fill_levels):
        """
        fill_levels: dict mit Füllständen in Milliliter
        Beispiel: {"water": 800, "syrup_a": 500, "syrup_b": 200, "alcohol": 300}
        """
        self.fill_levels = fill_levels

        # Rezepte mit festem Volumen (z. B. 200 ml)
        self.target_volume_ml = 200

        self.recipes = {
            "Cola-Mix":     {"water": 0.4, "syrup_a": 0.3,},
            "Cocktail":     {"alcohol": 0.4, "syrup_b": 0.2, "water": 0.4},
            "Schorle":      {"water": 0.5, "syrup_b": 0.5},
            "Light Mix":    {"water": 0.7, "syrup_a": 0.3}
        }

    def suggest_best_drink(self):
        best_drink = None
        max_possible_volume = 0

        for name, ingredients in self.recipes.items():
            volume = self._max_mixable_volume_ml(ingredients)
            if volume >= self.target_volume_ml and volume > max_possible_volume:
                best_drink = name
                max_possible_volume = volume

        if best_drink:
            print(f"Empfohlenes Getränk: {best_drink} (max. {int(max_possible_volume)} ml mischbar)")
            self._apply_recipe(best_drink)
            print("\nAktueller Füllstand nach Mischung:")
            for k, v in self.fill_levels.items():
                print(f"  {k}: {int(v)} ml")
        else:
            print("Kein Getränk mischbar mit aktuellem Füllstand.")

    def _max_mixable_volume_ml(self, recipe):
        max_volume = float('inf')
        for ingredient, fraction in recipe.items():
            available = self.fill_levels.get(ingredient, 0)
            possible_volume = available / fraction
            max_volume = min(max_volume, possible_volume)
        return max_volume

    def _apply_recipe(self, recipe_name):
        recipe = self.recipes[recipe_name]
        print(f"\nMische {self.target_volume_ml} ml {recipe_name}...")
        for ingredient, fraction in recipe.items():
            needed = self.target_volume_ml * fraction
            self.fill_levels[ingredient] -= needed

sensor_data = {
    "water": 800,
    "syrup_a": 300,
    "syrup_b": 100,
    "alcohol": 100
}

mixer = BeverageSuggestion(sensor_data)
mixer.suggest_best_drink()
