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

# Test-Pins
dout_pin = 2  # DOUT an GP2
sck_pin = 3   # SCK an GP3

# HX711 initialisieren
hx = HX711(dout=dout_pin, pd_sck=sck_pin)

print("Starte Messung...")

# Endlosschleife zum Testen
while True:
    rohwert = hx.read()
    gewicht_in_gramm = rohwert / 1000  # Dummy-Skalierung für Testzwecke!
    print(f"Rohwert: {rohwert}, Gewicht in Gramm (ungefähr!): {gewicht_in_gramm:.2f}")
    time.sleep(0.5)
