import time
import board
import digitalio
import usb_cdc
import json
from config import pump_pins, sensor_pins, totraum, flow_rate
from hx711 import HX711

# Pumpen-Setup
class PumpController:
    def __init__(self):
        self.flow_rate_ml_per_sec = flow_rate
        self.totraum = totraum
        self.pumps = {}
        for name, pin in pump_pins.items():
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.OUTPUT
            p.value = False
            self.pumps[name] = p

    def dispense(self, ingredient, amount_ml):
        if ingredient not in self.pumps:
            return f"Unbekannte Zutat: {ingredient}"

        pump = self.pumps[ingredient]
        duration = amount_ml / self.flow_rate_ml_per_sec
        duration_totraum = self.totraum.get(ingredient, 0) / self.flow_rate_ml_per_sec

        pump.value = True
        time.sleep(duration_totraum + duration)
        pump.value = False
        return f"{ingredient}: {amount_ml} ml abgegeben"

    def emergency_stop(self):
        for pump in self.pumps.values():
            pump.value = False

    def reset_pumps(self):
        for pump in self.pumps.values():
            pump.value = False

# Sensor-Setup
def read_sensor(dout_pin, sck_pin):
    hx = HX711(dout_pin, sck_pin)
    values = [hx.read() for _ in range(5)]
    avg = sum(values) / len(values)

    gain = 1300 / (6584035.0 - 7903406.0)
    offset = 7903406.0
    gewicht = gain * (avg - offset)
    return max(0, round(gewicht, 1))

def read_fill_levels():
    results = {}
    for name, dout in sensor_pins.items():
        if name == "SCK":
            continue
        results[name] = read_sensor(dout, sensor_pins["SCK"])
    return results

# Hauptlogik
def main_loop():
    pump_ctrl = PumpController()
    emergency = False

    while True:
        if usb_cdc.data.in_waiting:
            command = usb_cdc.data.read(usb_cdc.data.in_waiting).decode().strip()
            parts = command.split()

            if command == "READ_FILL_LEVELS":
                levels = read_fill_levels()
                usb_cdc.data.write((json.dumps(levels) + "\n").encode())

            elif parts[0] == "DISPENSE" and len(parts) == 3:
                if emergency:
                    usb_cdc.data.write(b"ERROR: NOT-AUS aktiv\n")
                    continue
                zutatenname = parts[1]
                try:
                    menge = float(parts[2])
                    result = pump_ctrl.dispense(zutatenname, menge)
                    usb_cdc.data.write((result + "\n").encode())
                except ValueError:
                    usb_cdc.data.write(b"ERROR: Ungültige Menge\n")

            elif command == "EMERGENCY_STOP":
                emergency = True
                pump_ctrl.emergency_stop()
                usb_cdc.data.write(b"NOT-AUS aktiviert\n")

            elif command == "RESET_PUMPS":
                emergency = False
                pump_ctrl.reset_pumps()
                usb_cdc.data.write(b"NOT-AUS zurückgesetzt\n")

            else:
                usb_cdc.data.write(b"Unbekannter Befehl\n")

        time.sleep(0.05)

main_loop()