# sensor_manager.py (PC-Seite)
import serial
import jsonx
from config import SERIAL_PORT, BAUDRATE

class SensorManager:
    def __init__(self):
        self.ser = None

    def read_fill_levels(self):
        try:
            with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2) as ser:
                ser.write(b"READ\n")  # Sende Befehl an den Pico
                raw = ser.readline().decode().strip()
                if raw:
                    data = json.loads(raw)
                    return data
                else:
                    print("Keine Daten empfangen.")
                    return {}
        except Exception as e:
            print(f"[SensorManager] Fehler bei der Verbindung: {e}")
            return {}

