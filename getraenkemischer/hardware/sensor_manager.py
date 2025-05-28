'''
Funktion:
- Liest die Sensoren und gibt in einem Dictionary zurück ob die Behälter voll oder leer sind

Klassen:
- SensorManager
    Klassenobjekte:
        - sensor_pins: dict
    Klassenmethoden:
        - __init__()
        - read_sensors() (gibt dict zurücj mit Zuordnung Pumpe:Pin)
'''
from config import SENSOR_PINS
from machine import Pin

class SensorManager:
    def __init__(self):

        # Zuordnung der Behälter zu den Pins
        self.sensor_pins = SENSOR_PINS

    # ordnet den Sensoren in einem Dictionary voll oder leer zu
    def read_sensors(self):
        results = {}
        for name, pin in self.sensor_pins.items():
            results[name] = pin.value()  # 1 = voll, 0 = leer
        return results