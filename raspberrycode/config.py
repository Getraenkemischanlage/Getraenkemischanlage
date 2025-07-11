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
import time

# Vereinfachter HX711-Treiber für Pico
class HX711:
    def __init__(self, dout, pd_sck):
        self.dout = Pin(dout, Pin.IN, pull=Pin.PULL_UP)
        self.pd_sck = Pin(pd_sck, Pin.OUT)
        self.pd_sck.value(0)

    def read(self):
        # Warten bis Daten bereit (DOUT = LOW)
        while self.dout.value() == 1:
            pass

        count = 0
        for _ in range(24):
            self.pd_sck.value(1)
            count = count << 1
            self.pd_sck.value(0)
            if self.dout.value():
                count += 1

        # 25. Taktimpuls für Kanal-/Verstärkungseinstellung
        self.pd_sck.value(1)
        count = count ^ 0x800000  # Zweierkomplement-Anpassung
        self.pd_sck.value(0)

        return count


class SensorManager:
    def __init__(self):
        self.sensor_pins = sensor_pins

    def read_fill_levels(self):
        self.gewicht_in_gramm = []
        self.zuordnung = {}

        # Sensoren außer "SCK" (angenommen: SCK ist für alle gleich)
        sensor_keys = list(self.sensor_pins.keys())
        data_keys = sensor_keys[1:]  # ["Wasser", "Sirup_a", "Sirup_b", "Alkohol"]

        for key in data_keys:
            dout = self.sensor_pins[key]
            pd_sck = self.sensor_pins["SCK"]
            print(f"[{key}] DOUT: {dout}, SCK: {pd_sck}")

            hx = HX711(dout, pd_sck)
            rohwerte = []

            for _ in range(10):
                rohwert = hx.read()
                rohwerte.append(rohwert)
                time.sleep(0.5)

            durchschnitt = sum(rohwerte) // len(rohwerte)

            # Beispielhafte Kalibrierung – muss angepasst werden
            gain = 1300 / (6584035.0 - 7903406.0)
            offset = 7903406.0
            gewicht = gain * (durchschnitt - offset)

            self.gewicht_in_gramm.append(gewicht)
            self.zuordnung[key] = gewicht

            print(f"[{key}] Rohwert: {durchschnitt}, Gewicht (ca.): {gewicht:.2f} g")
            time.sleep(0.5)

        return self.zuordnung


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