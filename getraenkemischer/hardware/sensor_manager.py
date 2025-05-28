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

Anschlüsse der Sensoren an den Raspberry Pi:
- Sensor 1: GP 0
- Sensor 2: GP 1
- Sensor 3: GP 2
- Sensor 4: GP 3
- Sensor 5: GP 4

'''

from machine import Pin

class SensorManager:
    def __init__(self):

        # Zuordnung der Behälter zu den Pins
        self.sensor_pins = {
            "Wasser":  Pin(10, Pin.IN),   # Sensor an GPIO 0
            "Sirup_a": Pin(11, Pin.IN),   # Sensor an GPIO 1
            "Sirup_b": Pin(14, Pin.IN),   # Sensor an GPIO 2
            "Sirup_c": Pin(15, Pin.IN),   # Sensor an GPIO 3
            "Alkohol": Pin(4, Pin.IN)    # Sensor an GPIO 4
        }

    # ordnet den Sensoren in einem Dictionary voll oder leer zu
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