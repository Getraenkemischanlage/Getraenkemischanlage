# sensor_main.py (Pico-Seite – wird auf dem Mikrocontroller ausgeführt)
'''import board
import digitalio
import time
import usb_cdc
import json
from hx711 import HX711  

# Pin-Zuweisung
SCK = board.GP0
SENSORS = {
    "Wasser": board.GP1,
    "Sirup_a": board.GP2,
    "Sirup_b": board.GP3,
    "Sirup_c": board.GP4
}

def read_sensor(dout_pin):
    hx = HX711(dout_pin, SCK)
    values = [hx.read() for _ in range(5)]
    avg = sum(values) / len(values)
    # Beispielkalibrierung
    gain = 1300 / (6584035.0 - 7903406.0)
    offset = 7903406.0
    gewicht = gain * (avg - offset)
    return max(0, round(gewicht, 1))  # Kein negativer Füllstand

def main_loop():
    while True:
        if usb_cdc.data.in_waiting:
            command = usb_cdc.data.read(usb_cdc.data.in_waiting).decode().strip()
            if command == "READ":
                results = {}
                for name, pin in SENSORS.items():
                    results[name] = read_sensor(pin)
                json_data = json.dumps(results)
                usb_cdc.data.write((json_data + "\n").encode())

        time.sleep(0.1)

main_loop()
'''