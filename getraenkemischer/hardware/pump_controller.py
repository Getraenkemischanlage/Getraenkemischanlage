'''
Funktion:
- Steuert die Pumpen an 

Klassen: 
- PumpController
    Klassenobjekte:
    - pump_pins: dict
    - flow_rate_ml_per_sec: float
    - pumps: dict
    Klassenmethoden:
    - __init__()
    - dispense(ingredient: str, amount_ml: float)


'''
from config import PUMP_PINS, FLOW_RATE
from logic.mixer_controller import MixerController
import time

class PumpController:
    def __init__(self):       
        self.pump_pins = PUMP_PINS  # Zuordnung der Pumpen zu den Pins

        self.flow_rate_ml_per_sec = FLOW_RATE  # Durchflussrate: z. B. 10 ml/s

    
    '''
    def test(self):             # Testmethode
        pumpe = self.pump_pins["Wasser"]  # Beispiel für eine Pumpe, z. B. Wasser

        while True:
            print("Pumpe AN")
            pumpe.value(1)  # Pumpe einschalten
            time.sleep(2)   # 2 Sekunden warten

            print("Pumpe AUS")
            pumpe.value(0)  # Pumpe ausschalten
            time.sleep(2)   # 2 Sekunden warten
    '''

    def dispense(self, ingredient, amount_ml):
        # Berechnung der Förderzeit
        duration = amount_ml / self.flow_rate_ml_per_sec
        
        # Auswahl der richtigen Pumpe
        pump = self.pump_pins[ingredient]

        # Ausgabe für den Benutzer
        print(f"Zutat {ingredient}: {amount_ml} ml ausgeben ({duration:.2f} Sekunden)")

        # Pumpe aktivieren
        pump.value(1)
        time.sleep(duration)
        pump.value(0)


pump_controller = PumpController()  # Erstellen eines PumpController-Objekts
#pump_controller.test()  # Testen der Pumpensteuerung
pump_controller.dispense("Wasser", 100)  # Beispielaufruf zum Fördern von 100 ml Wasser
    