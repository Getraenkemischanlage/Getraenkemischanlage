'''
Testprogramm zum anteuern der Pumpen
Muss auf dem Pico ausgeführt werden
'''

import board
import digitalio
import time

# Pumpen direkt benennen
pumpe1 = digitalio.DigitalInOut(board.GP16)
pumpe1.direction = digitalio.Direction.OUTPUT

pumpe2 = digitalio.DigitalInOut(board.GP17)
pumpe2.direction = digitalio.Direction.OUTPUT

pumpe3 = digitalio.DigitalInOut(board.GP20)
pumpe3.direction = digitalio.Direction.OUTPUT

pumpe4 = digitalio.DigitalInOut(board.GP21)
pumpe4.direction = digitalio.Direction.OUTPUT

# Test: Jede Pumpe für 2 Sekunden einschalten
print("Pumpe 1 EIN")
pumpe1.value = True
time.sleep(2)
pumpe1.value = False
print("Pumpe 1 AUS")
time.sleep(1)

print("Pumpe 2 EIN")
pumpe2.value = True
time.sleep(2)
pumpe2.value = False
print("Pumpe 2 AUS")
time.sleep(1)

print("Pumpe 3 EIN")
pumpe3.value = True
time.sleep(2)
pumpe3.value = False
print("Pumpe 3 AUS")
time.sleep(1)

print("Pumpe 4 EIN")
pumpe4.value = True
time.sleep(2)
pumpe4.value = False
print("Pumpe 4 AUS")

