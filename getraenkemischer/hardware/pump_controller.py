'''
Steuert die Pumpen an 

Anschlüsse der Pumpen an den Raspberry Pi:
Pumpe 1: GP 22
Pumpe 2: GP 21
Pumpe 3: GP 20
Pumpe 4: GP 19
Pumpe 5: GP 18

'''
from machine import Pin
import time

class PumpController:
    def __init__(self):       
        # Zuordnung der Pumpen zu den Pins
        self.pump_pins = {
            "Wasser": 22,     
            "Sirup_a": 21,    
            "Sirup_b": 20,    
            "Sirup_c": 19,
            "Alkohol": 18     
        }

        self.flow_rate_ml_per_sec = 10  # Durchflussrate: z. B. 10 ml/s

        self.pumps = {}                 # Wird später mit Pin-Objekten gefüllt

        self.set_pumps()              # Initialisierungsmethode aufrufen

    def set_pumps(self):
        #Initialisiert alle Pumpen-Pins als Ausgang
        for name, pin_number in self.pump_pins.items():
            self.pumps[name] = Pin(pin_number, Pin.OUT)


    def dispense(self, ingredient, amount_ml):
        if ingredient not in self.pumps:
            print(f"Ingredient '{ingredient}' is not assigned to any pump.")
            return

        duration = amount_ml / self.flow_rate_ml_per_sec
        pump = self.pumps[ingredient]

        print(f"Dispensing {ingredient}: {amount_ml} ml ({duration:.2f} seconds)")

        if pump:
            pump.value(1)
            time.sleep(duration)
            pump.value(0)
        else:
            time.sleep(duration)  # Simulation delay