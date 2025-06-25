'''
Funktion:
- Steuert die Pumpen an 

Klassen: 
- PumpController
    Klassenobjekte:
    - pump_pins: dict
    - flow_rate_ml_per_sec: float
    Klassenmethoden:
    - __init__()
    - dispense(ingredient: str, amount_ml: float)
'''

from config import pump_pins, sensor_pins, totraum, flow_rate, target_volume
import time

class PumpController():
    def __init__(self):  
        self.pump_pins = pump_pins              # Zuordnung der Pumpen zu den Pins
        self.totraum = totraum                  # Zuordnung der Toträume zu den Zutaten
        self.flow_rate_ml_per_sec = flow_rate   # Durchflussrate: z. B. 10 ml/s


    def dispense(self, ingredient, amount_ml):
        # Berechnung der Förderzeit
        duration = amount_ml / self.flow_rate_ml_per_sec
        duration_totraum = self.totraum[ingredient] / self.flow_rate_ml_per_sec
        # Auswahl der richtigen Pumpe
        pump = self.pump_pins[ingredient]

        # Ausgabe für den Benutzer (nur zum Testen)
        # print(f"Zutat {ingredient}: {amount_ml} ml ausgeben ({duration:.2f} Sekunden)")

        # Pumpe aktivieren
        pump.value(1)
        time.sleep(duration_totraum)
        time.sleep(duration)
        pump.value(0)

    
    def emergency_stop(self):
        # Alle Pumpen ausschalten
        for pump in self.pump_pins.values():
            pump.value(0)
        print("Alle Pumpen gestoppt.")

    def get_pump_status(self):
        # Gibt den Status aller Pumpen zurück
        status = {ingredient: pump.value() for ingredient, pump in self.pump_pins.items()}
        return status
    
    def reset_pumps(self):
        # Setzt alle Pumpen auf den Ausgangszustand (aus)
        for pump in self.pump_pins.values():
            pump.value(0)
        print("Alle Pumpen zurückgesetzt.")

    





    