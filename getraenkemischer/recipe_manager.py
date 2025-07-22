import json
import os

'''
Rezeptverwaltung

Klassen:
- Recipe Manager
    Klassenobjekte:
    -   recipe: dict
    Klassenmethoden:
    - __init__()
    - get_all_recipes()     (gibt alle Rezepte zurück)
    - get_recipes(name: str)    (Gibt ein bestimmtes Rezept nach Name zurück.)

'''

class RecipeManager:
    def __init__(self, recipe_file="recipes.json"):
        self.recipe_file = recipe_file
        self.load_recipes()

    def load_recipes(self):
        """Load recipes from JSON file"""
        try:
            if os.path.exists(self.recipe_file):
                with open(self.recipe_file, 'r') as f:
                    self.recipes = json.load(f)
            else:
                # Default recipes if file doesn't exist
                self.recipes = {
                    "Cola-Mix": {"Wasser": 60, "Sirup_a": 140},
                    "Cocktail": {"Sirup_c": 80, "Sirup_b": 40, "Wasser": 80},
                    "Schorle": {"Wasser": 100, "Sirup_b": 100},
                    "Cola-Light Mix": {"Wasser": 140, "Sirup_a": 60}
                }
                # Save default recipes
                self.save_recipes()
        except Exception as e:
            print(f"Error loading recipes: {e}")
            self.recipes = {}

    def save_recipes(self):
        """Save recipes to JSON file"""
        try:
            with open(self.recipe_file, 'w') as f:
                json.dump(self.recipes, f, indent=4)
        except Exception as e:
            print(f"Error saving recipes: {e}")

    def get_all_recipes(self):
        return self.recipes

    def get_recipe(self, name):
        return self.recipes.get(name)

    def add_recipe(self, name, recipe):
        """Add or update a recipe"""
        self.recipes[name] = recipe
        self.save_recipes()

    def delete_recipe(self, name):
        """Delete a recipe"""
        if name in self.recipes:
            del self.recipes[name]
            self.save_recipes()
