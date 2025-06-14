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


from config import PUMP_PINS, FLOW_RATE
import time


class PumpController:
    def __init__(self):       
        self.pump_pins = PUMP_PINS  # Zuordnung der Pumpen zu den Pins

        self.flow_rate_ml_per_sec = FLOW_RATE  # Durchflussrate: z. B. 10 ml/s


    def dispense(self, ingredient, amount_ml):
        # Berechnung der Förderzeit
        duration = amount_ml / self.flow_rate_ml_per_sec
        
        # Auswahl der richtigen Pumpe
        pump = self.pump_pins[ingredient]

        # Ausgabe für den Benutzer (nur zum Testen)
        # print(f"Zutat {ingredient}: {amount_ml} ml ausgeben ({duration:.2f} Sekunden)")

        # Pumpe aktivieren
        pump.value(1)
        time.sleep(duration)
        pump.value(0)



    