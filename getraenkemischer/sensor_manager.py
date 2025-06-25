'''
Funktion:
- Liest die Sensoren ein 
- Berechnet den Füllstand der Behälter
- Gibt die Füllstände der Behälter zurück

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
from machine import Pin
import time

# Vereinfachter HX711-Treiber für den Test
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

'''
# Test-Pins
dout_pin = 1  # DOUT an GP2
sck_pin = 0   # SCK an GP3

# HX711 initialisieren
hx = HX711(dout=dout_pin, pd_sck=sck_pin)
'''

class SensorManager:
    def __init__(self):
        self.sensor_pins = SENSOR_PINS
        self.gewicht_in_gramm = []
        self.zuordnung = {}  # Zuordnung von Behäälter zu Gewichten
       
    def read_sensors(self):
        for i in range(1, 4):
            dout = list(self.sensor_pins.values())[i]
            pd_sck = self.sensor_pins["SCK"]
            print(f"dout: {dout}, pd_sck: {pd_sck}")
            hx = HX711(dout, pd_sck)  

            print(f"Starte Messung Sensor {list(self.sensor_pins.keys())[i]} ")

            rohwerte = []  # Liste für Rohwerte
            for _ in range(10):         # Anzahl der Messungen pro Sensor
                rohwert = hx.read()  # Rohwert vom HX711 lesen
                rohwerte.append(rohwert)  
                time.sleep(0.5)
                
            durchschittswert = sum(rohwerte) // len(rohwerte)  # Durchschnitt der Rohwerte

            gain = 1300 / (1.160204e+07 - 1.156051e+07)  
            offset = 1.156051e+07

            self.gewicht_in_gramm.append(gain * (durchschittswert - offset))

            for i in range(len(self.gewicht_in_gramm)):
                self.zuordnung["Sensor_" + str(i)] = self.gewicht_in_gramm[i]
                
            print(f"Rohwert: {durchschittswert}, Gewicht in Gramm (ungefähr!): {self.gewicht_in_gramm:.2f}")
            time.sleep(0.5)

        return self.zuordnung

'''
    def calculate_fill_level(self):
        for name, weight in self.read_sensors().items():
            # Beispiel: 1g = 1ml, anpassen je nach Behälter!
            fill_level[name] = max(0, int(weight))
        return fill_level
'''

'''
# Endlosschleife zum Testen

print("Starte Messung...")

while True:
    rohwert = hx.read()

    gain = 1300 / (1.160204e+07 - 1.156051e+07)  
    offset = 1.156051e+07

    gewicht_in_gramm = gain * (rohwert - offset)

    print(f"Rohwert: {rohwert}, Gewicht in Gramm (ungefähr!): {gewicht_in_gramm:.2f}")
    time.sleep(0.5)


# Methode zum Kalibrieren

for i in range(20):
    liste = []
    liste.append(hx.read())
    time.sleep(0.5)
    durchschnitt = sum(liste) / len(liste)

print(durchschnitt)
'''