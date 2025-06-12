'''
zentrale Konfiguration der Pins und Flussrate

Anschlüsse der Pumpen an den Raspberry Pi:
- Pumpe 1: GP 22
- Pumpe 2: GP 21
- Pumpe 3: GP 20
- Pumpe 4: GP 19
- Pumpe 5: GP 18

Anschlüsse der Sensoren an den Raspberry Pi:
- DT: GP 2
- SCK: GP 3
'''
from machine import Pin


# GPIO-Zuordnung der Pumpen
PUMP_PINS = {
    "Wasser":  Pin(22, Pin.OUT),
    "Sirup_a": Pin(25, Pin.OUT),
    "Sirup_b": Pin(26, Pin.OUT),
    "Sirup_c": Pin(27, Pin.OUT),
    "Alkohol": Pin(29, Pin.OUT)
}


# GPIO-Zuordnung der Sensoren
SENSOR_PINS = {
    "SCK": Pin(0, Pin.OUT),         # Serial Clock GP0
    "Sensor_1": Pin(1, Pin.IN),     # Sensor 1 GP1
    "Sensor_2": Pin(2, Pin.IN),     # Sensor 2 GP2
    "Sensor_3": Pin(3, Pin.IN),     # Sensor 3 GP3 
    "Sensor_4": Pin(4, Pin.IN),     # Sensor 4 GP4
    "Sensor_5": Pin(5, Pin.IN)      # Sensor 5 GP5
        }

    
FLOW_RATE = 10                  # Fördermenge pro Pumpe in ml/s

target_volume = 200             # Zielmenge in ml