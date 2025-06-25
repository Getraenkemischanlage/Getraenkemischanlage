from machine import Pin
import time

# Pumpe/LED an GPIO 22
pumpe = Pin(16, Pin.OUT)

print("Starte Pumpentest...")

while True:
    print("Pumpe EIN")
    pumpe.value(1)      # Setzt GP22 auf HIGH
    time.sleep(5)       # 2 Sekunden an
    

    print("Pumpe AUS")
    pumpe.value(0)      # Setzt GP22 auf LOW
    time.sleep(2)       # 2 Sekunden aus
