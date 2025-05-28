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
    "Wasser":  Pin(24, Pin.OUT),
    "Sirup_a": Pin(25, Pin.OUT),
    "Sirup_b": Pin(26, Pin.OUT),
    "Sirup_c": Pin(27, Pin.OUT),
    "Alkohol": Pin(29, Pin.OUT)
}


# GPIO-Zuordnung der Sensoren
SENSOR_PINS = {
            "Wasser":  Pin(1, Pin.IN),   
            "Sirup_a": Pin(2, Pin.IN),   
            "Sirup_b": Pin(4, Pin.IN),   
            "Sirup_c": Pin(5, Pin.IN),  
            "Alkohol": Pin(6, Pin.IN)    
        }

    
FLOW_RATE = 10                  # Fördermenge pro Pumpe in ml/s

target_volume = 200             # Zielmenge in ml