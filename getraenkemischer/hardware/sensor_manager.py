'''
Funktion:
- Liest die Sensoren ein 
- Berechnet den Füllstand der Behälter
- Gibt die Füllstände der Behälter zurück
- Gibt die leeren Behälter zurück

Klassen:
- SensorManager
    Klassenobjekte:
        - sensor_pins: dict
        - fill_level: dict
    Klassenmethoden:
        - __init__()
        - read_sensors() (gibt dict zurücj mit Zuordnung Pumpe:Pin)
        - calculate_fill_level
'''

from config import SENSOR_PINS
from hx711py-master.hx711 import HX711

class SensorManager:
    def __init__(self):
        self.sensor_pins = SENSOR_PINS
        self.hx_sensors = {}
        for name, (dt, sck) in self.sensor_pins.items():
            self.hx_sensors[name] = HX711(dt, sck)
            self.hx_sensors[name].set_reading_format("MSB", "MSB")
            self.hx_sensors[name].set_reference_unit(1)  # Kalibrierwert anpassen!
            self.hx_sensors[name].reset()
            self.hx_sensors[name].tare()

    def read_sensors(self):
        results = {}
        for name, hx in self.hx_sensors.items():
            results[name] = hx.get_weight(5)  # Mittelwert aus 5 Messungen
        return results

    def calculate_fill_level(self):
        fill_level = {}
        for name, weight in self.read_sensors().items():
            # Beispiel: 1g = 1ml, anpassen je nach Behälter!
            fill_level[name] = max(0, int(weight))
        return fill_level


    '''
    def leere_behaelter(self):          #Rückgabe: Liste aller leeren Behälter
        
        return [name for name, val in self.read_sensors().items() if val == 0]
    '''
