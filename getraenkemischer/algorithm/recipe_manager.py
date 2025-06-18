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
    def __init__(self):
        self.recipes = {
            "Cola-Mix":         {"Wasser": 60, "Sirup_a": 140,},
            "Cocktail":         {"Alkohol": 80, "Sirup_b": 40, "Wasser": 80},
            "Schorle":          {"Wasser": 100, "Sirup_b": 100},
            "Cola-Light Mix":   {"Wasser": 140, "Sirup_a": 60}
        }

    def get_all_recipes(self):
        return self.recipes

    def get_recipe(self, name):
        return self.recipes.get(name)
