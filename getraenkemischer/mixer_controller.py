'''
zentrale Steuereinheit, die ein Rezept ausführt, indem sie die entsprechenden Pumpen für eine bestimmte Zeit aktiviert

Klassen:
- MixerController:
    Klassenobjekte:
    - recipe_manager: RecipeManager
    - pump_controller: PumpController
    - target_volume_ml: int
    Klassenmethoden:
    - __init__(pump_controller: PumpController)
    - mix(recipe_name: str)     (gibt None zurück)
'''
'''
import time
from getraenkemischer.algorithm.recipe_manager import RecipeManager
from config import target_volume
from hardware.pump_controller import PumpController


class MixerController:
    def __init__(self, pump_controller):
        self.recipe_manager = RecipeManager()           # Erstellt ein Objekt zum Zugriff auf die Rezeptdaten
        self.pump_controller = pump_controller          # Referenz auf den PumpController
        self.target_volume_ml = target_volume           # Zielmenge in ml, aus der zentralen Konfiguration

    def mix(self, recipe_name):                         # Holt das entsprechende Rezept
        recipe = self.recipe_manager.get_recipe(recipe_name)
        if not recipe:
            print(f"Rezept '{recipe_name}' nicht gefunden.")
            return

        print(f"Starte Mischung: {recipe_name}")        # Gehe alle Zutaten im Rezept durch und berechne die Fördermenge
        for ingredient, ratio in recipe.items():
            amount = self.target_volume_ml * ratio
            self.pump_controller.dispense(ingredient, amount)



            
    def dispense(self, ingredient, amount_ml):
        #Jeweilige Pumpe wird so lange angesteuert bis gewünschte Menge erreicht ist
        #Bekommt ingridient (Welche Flüssigkeit soll gefördert werden?) und amount_ml (Welche Menge) übermittelt

        #Überprüfung ob für Zutat eine Pumpe vorhanden ist
        if ingredient not in self.pumps:
            print(f"Zutat '{ingredient}' ist keiner Pumpe zugewiesen.")
            return

        #Berechnung der Förderzeit
        duration = amount_ml / self.flow_rate_ml_per_sec
        
        #Auswahl der richtigen Pumpe
        pump = self.pumps[ingredient]

        #Ausgabe für Benutzer
        print(f"Zutat {ingredient}: {amount_ml} ml ausgeben ({duration:.2f} Sekunden)")

        #Pumpe aktivieren
        pump.value(1)
        time.sleep(duration)
        pump.value(0)

'''
