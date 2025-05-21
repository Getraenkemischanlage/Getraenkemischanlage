from hardware.sensor_manager import SensorManager

class BeverageSuggestion:
    def __init__(self, fill_levels):
        """
        fill_levels: dict mit Füllständen in Milliliter
        Beispiel: {"Wasser": 800, "Sirup_a": 500, "Sirup_b": 200, "Alkohol": 300}
        """
        self.fill_levels = fill_levels

        # Rezepte mit festem Volumen (z. B. 200 ml).
        self.target_volume_ml = 200

        self.recipes = {
            "Cola-Mix":     {"Wasser": 0.4, "Sirup_a": 0.3,},
            "Cocktail":     {"Alkohol": 0.4, "Sirup_b": 0.2, "Wasser": 0.4},
            "Schorle":      {"Wasser": 0.5, "Sirup_b": 0.5},
            "Cola-Light Mix":    {"Wasser": 0.7, "Sirup_a": 0.3}
        }

    def suggest_best_drink(self):
        best_drink = None
        max_possible_volume = 0

        for name, ingredients in self.recipes.items():
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
            possible_volume = available / fraction
            max_volume = min(max_volume, possible_volume)
        return max_volume

    def apply_recipe(self, recipe_name):
        recipe = self.recipes[recipe_name]
        print(f"\nMische {self.target_volume_ml} ml {recipe_name}...")
        for ingredient, fraction in recipe.items():
            needed = self.target_volume_ml * fraction
            self.fill_levels[ingredient] -= needed

sensor_manager = SensorManager()
current_fill_levels = sensor_manager.read_fill_levels()

mixer = BeverageSuggestion(current_fill_levels)
mixer.suggest_best_drink()
