from config import sensor_pins
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