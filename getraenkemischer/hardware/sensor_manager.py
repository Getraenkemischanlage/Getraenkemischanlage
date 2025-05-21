# Sensor 1: GP 0
# Sensor 2: GP 1
# Sensor 3: GP 2
# Sensor 4: GP 3
# Sensor 5: GP 4

# Wir importieren die Pin-Klasse aus der machine-Bibliothek,
# damit wir die GPIO-Pins des Raspberry Pi Pico benutzen können.

from machine import Pin

class SensorManager:
    def __init__(self, volume_per_tank=500):
        #volume_per_tank: Wieviel ml in einem Behälter sind, wenn der Sensor 'voll' meldet
        
        self.volume_per_tank = volume_per_tank  

        # Hier ordnen wir jedem Behälter einen bestimmten GPIO-Pin zu.
        # Die Sensoren sind so angeschlossen, dass sie bei "voll" ein HIGH-Signal (1) liefern.
        self.sensor_pins = {
            "Wasser": Pin(0, Pin.IN, Pin.PULL_DOWN),     # Sensor an GPIO 0
            "Sirup_a": Pin(1, Pin.IN, Pin.PULL_DOWN),   # Sensor an GPIO 1
            "Sirup_b": Pin(2, Pin.IN, Pin.PULL_DOWN),   # Sensor an GPIO 2
            "Alkohol": Pin(4, Pin.IN, Pin.PULL_DOWN)    # Sensor an GPIO 4
        }

    def read_fill_levels(self):
        #Liest den Zustand aller Sensoren aus und gibt ein Dictionary mit dem Namen des Behälters und der aktuellen Füllmenge in ml zurück.

        levels = {}  # Hier speichern wir die Ergebnisse

        # Wir gehen alle Sensoren durch
        for name, pin in self.sensor_pins.items():
            if pin.value() == 1:
                # Wenn der Sensor aktiviert ist (Behälter voll)
                levels[name] = self.volume_per_tank
            else:
                # Wenn der Sensor deaktiviert ist (Behälter leer)
                levels[name] = 0

        return levels
