from machine import Pin
import time

# HX711-Treiber für MicroPython (vereinfachte Version)
class HX711:
    def __init__(self, dout, pd_sck):
        self.dout = Pin(dout, Pin.IN, pull=Pin.PULL_UP)
        self.pd_sck = Pin(pd_sck, Pin.OUT)
        self.pd_sck.value(0)

    def read(self):
        # Warten bis Datenpin LOW ist
        while self.dout.value() == 1:
            pass

        count = 0
        for _ in range(24):
            self.pd_sck.value(1)
            count = count << 1
            self.pd_sck.value(0)
            if self.dout.value():
                count += 1

        # 25. Puls für die Kanal- und Verstärker-Einstellung
        self.pd_sck.value(1)
        count = count ^ 0x800000  # Zweierkomplement
        self.pd_sck.value(0)

        return count

# Pins anpassen:
dout_pin = 2  # z.B. GPIO 2
sck_pin = 3   # z.B. GPIO 3

hx = HX711(dout=dout_pin, pd_sck=sck_pin)

print("Starte Messung...")

while True:
    gewicht = hx.read()
    gewicht_in_gramm = gewicht / 1000
    print(f"Gewicht in Gramm: {gewicht_in_gramm:.2f}")
    time.sleep(0.5)
    

