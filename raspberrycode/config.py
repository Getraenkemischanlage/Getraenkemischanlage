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
- Rot zu E+, Schwarz zu E-, Grün zu A+ und Weiß zu A-
'''

from machine import Pin


# GPIO-Zuordnung der Pumpen
pump_pins = {
    "Wasser":  Pin(16, Pin.OUT),
    "Sirup_a": Pin(17, Pin.OUT),
    "Sirup_b": Pin(20, Pin.OUT),
    "Sirup_c": Pin(21, Pin.OUT),
}


# GPIO-Zuordnung der Sensoren
sensor_pins = {
    "SCK": Pin(0, Pin.OUT),         # Serial Clock GP0
    "Wasser": Pin(1, Pin.IN),       # Sensor 1 GP1
    "Sirup_a": Pin(2, Pin.IN),      # Sensor 2 GP2
    "Sirup_b": Pin(3, Pin.IN),      # Sensor 3 GP3 
    "Sirup_c": Pin(4, Pin.IN),      # Sensor 4 GP4
        }

totraum = {
    "Wasser": 100,                # Gesamtvolumen Wasser in ml
    "Sirup_a": 100,                 # Gesamtvolumen Sirup A in ml
    "Sirup_b": 100,                 # Gesamtvolumen Sirup B in ml
    "Sirup_c": 100,                 # Gesamtvolumen Sirup C in ml
        }

flow_rate = 100                 # Fördermenge pro Pumpe in ml/s
target_volume = 400             # Zielmenge in ml