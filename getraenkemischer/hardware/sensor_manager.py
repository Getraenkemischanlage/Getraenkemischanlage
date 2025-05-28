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

class SensorManager:
    def __init__(self):

        # Zuordnung der Behälter zu den Pins
        self.sensor_pins = SENSOR_PINS

    # ordnet den Sensoren in einem Dictionary den Füllstand zu
    def read_sensors(self):
        results = {}
        for name, pin in self.sensor_pins.items():
            results[name] = pin.value()  # 1 = voll, 0 = leer
        return results
    
    def leere_behaelter(self):
        """
        Rückgabe: Liste aller leeren Behälter
        """
        return [name for name, val in self.read_sensors().items() if val == 0]

    def print_sensor_status(self):
        """
        Gibt den aktuellen Zustand der Sensoren lesbar aus
        """
        status = self.get_status_strings()
        for name, zustand in status.items():
            print(f"{name}: {zustand}")