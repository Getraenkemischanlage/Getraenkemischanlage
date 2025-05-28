'''
zentrale Konfiguration der Pins und Flussrate

Anschlüsse der Pumpen an den Raspberry Pi:
- Pumpe 1: GP 22
- Pumpe 2: GP 21
- Pumpe 3: GP 20
- Pumpe 4: GP 19
- Pumpe 5: GP 18

Anschlüsse der Sensoren an den Raspberry Pi:
- Sensor 1: GP 0
- Sensor 2: GP 1
- Sensor 3: GP 2
- Sensor 4: GP 3
- Sensor 5: GP 4
'''
from machine import Pin


# GPIO-Zuordnung der Pumpen
PUMP_PINS = {
    "Wasser":  Pin(1, Pin.OUT),
    "Sirup_a": Pin(21, Pin.OUT),
    "Sirup_b": Pin(20, Pin.OUT),
    "Sirup_c": Pin(19, Pin.OUT),
    "Alkohol": Pin(18, Pin.OUT)
}


# GPIO-Zuordnung der Sensoren
SENSOR_PINS = {
            "Wasser":  Pin(10, Pin.IN),   # Sensor an GPIO 0
            "Sirup_a": Pin(11, Pin.IN),   # Sensor an GPIO 1
            "Sirup_b": Pin(14, Pin.IN),   # Sensor an GPIO 2
            "Sirup_c": Pin(15, Pin.IN),   # Sensor an GPIO 3
            "Alkohol": Pin(4, Pin.IN)    # Sensor an GPIO 4
        }

    
FLOW_RATE = 10  # ml/sec

target_volume = 200 # Zielmenge in ml