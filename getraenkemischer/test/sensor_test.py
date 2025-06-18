from machine import Pin
from hx711 import HX711
import time

# HX711: DT an GPIO 4, SCK an GPIO 5
hx = HX711(d_out=Pin(4), pd_sck=Pin(5))

# Kalibrierfaktor festlegen (später feinjustieren!)
hx.set_scale(200)  # Dieser Wert muss kalibriert werden
hx.tare()          # Nullpunkt setzen

print("Starte Gewichtsmessung...")

while True:
    gewicht = hx.get_units(10)  # Durchschnitt aus 10 Messungen
    print("Gewicht: {:.2f} g".format(gewicht))
    time.sleep(1)
