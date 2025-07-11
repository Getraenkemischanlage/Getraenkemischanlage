import time
from config import pump_pins, totraum, flow_rate
import digitalio
import board

class PumpController:
    def __init__(self):
        self.flow_rate_ml_per_sec = flow_rate
        self.totraum = totraum

        # Pins initialisieren
        self.pumps = {}
        for name, pin in pump_pins.items():
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.OUTPUT
            p.value = False
            self.pumps[name] = p

    def dispense(self, ingredient, amount_ml):
        if ingredient not in self.pumps:
            print(f"Unbekannte Pumpe: {ingredient}")
            return

        pump = self.pumps[ingredient]
        duration = amount_ml / self.flow_rate_ml_per_sec
        duration_totraum = self.totraum.get(ingredient, 0) / self.flow_rate_ml_per_sec

        # Pumpe starten
        pump.value = True
        time.sleep(duration_totraum + duration)
        pump.value = False
        print(f"{ingredient}: {amount_ml} ml abgegeben")

    def emergency_stop(self):
        for pump in self.pumps.values():
            pump.value = False
        print("Alle Pumpen gestoppt.")

    def reset_pumps(self):
        for pump in self.pumps.values():
            pump.value = False
        print("Pumpen zurückgesetzt.")
