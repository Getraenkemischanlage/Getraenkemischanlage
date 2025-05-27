'''
Rezeptverwaltung

Klassen:
- Recipe Manager
    Klassenobjekte:
    -   reciped: dict
    Klassenmethoden:
    - __init__()
    - get_all_recipes()     (gibt alle Rezepte zurück)
    - get_recipes(name: str)    (Gibt ein bestimmtes Rezept nach Name zurück.)

'''

class RecipeManager:
    def __init__(self):
        self.recipes = {
            "Cola-Mix":         {"Wasser": 0.3, "Sirup_a": 0.7,},
            "Cocktail":         {"Alkohol": 0.4, "Sirup_b": 0.2, "Wasser": 0.4},
            "Schorle":          {"Wasser": 0.5, "Sirup_b": 0.5},
            "Cola-Light Mix":   {"Wasser": 0.7, "Sirup_a": 0.3}
        }

    def get_all_recipes(self):
        return self.recipes

    def get_recipe(self, name):
        return self.recipes.get(name)
