from machine import Pin

class SensorManager:
    def __init__(self, volume_per_tank=500):
        self.volume_per_tank = volume_per_tank  # ml bei Sensor = "voll"
        self.sensor_pins = {
            # Sensor 1: GP 0
            # Sensor 2: GP 1
            # Sensor 3: GP 2
            # Sensor 4: GP 3
            # Sensor 5: GP 4
            "water": Pin(0, Pin.IN, Pin.PULL_DOWN),
            "syrup_a": Pin(1, Pin.IN, Pin.PULL_DOWN),
            "syrup_b": Pin(2, Pin.IN, Pin.PULL_DOWN),
            "alcohol": Pin(4, Pin.IN, Pin.PULL_DOWN)
        }

    def read_fill_levels(self):
        levels = {}
        for name, pin in self.sensor_pins.items():
            levels[name] = self.volume_per_tank if pin.value() else 0
        return levels