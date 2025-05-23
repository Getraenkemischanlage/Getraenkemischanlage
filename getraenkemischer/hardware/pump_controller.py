# Pumpe 1: GP 22
# Pumpe 2: GP 21
# Pumpe 3: GP 20
# Pumpe 4: GP 19
# Pumpe 5: GP 18

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

        self.flow_rate_ml_per_sec = 10  # Flow rate: 10 ml/sec (Testwert)
    
        try:
            from machine import Pin
            self.pumps = {
                name: Pin(pin, Pin.OUT)
                for name, pin in self.pump_pins.items()
            }
        except ImportError:
            print("GPIO not available – simulation mode active.")
            self.pumps = {name: None for name in self.pump_pins}

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