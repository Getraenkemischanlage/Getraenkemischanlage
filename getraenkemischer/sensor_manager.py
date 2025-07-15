# sensor_manager.py (PC-Seite)
import serial
import json
import time
from config import SERIAL_PORT, BAUDRATE

# Passe diese Werte ggf. an
SERIAL_PORT = "COM5"
BAUDRATE = 9600

SENSOR_KEYS = ["Wasser", "Sirup_a", "Sirup_b", "Sirup_c"]

class SensorManager:
    def __init__(self):
        self.ser = None
        self.connect()

    def connect(self):
        if self.ser is None or not self.ser.is_open:
            try:
                print(f"Attempting to connect to {SERIAL_PORT}...")
                self.ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=5)
                time.sleep(2)  # Give more time for connection to stabilize
                print("Serial connection established")
                return True
            except Exception as e:
                print(f"Connection failed: {e}")
                self.ser = None
                return False
        return True

    def read_fill_levels(self):
        if not self.connect():
            return {}

        try:
            print("Sending READ command...")
            self.ser.reset_input_buffer()
            self.ser.write(b"READ\n")
            self.ser.flush()
            
            time.sleep(0.5)  # Increased wait time
            
            if self.ser.in_waiting:
                raw = self.ser.readline().decode().strip()
                print(f"Raw data received: {raw}")
                
                if raw:
                    try:
                        data = json.loads(raw)
                        if all(key in data for key in SENSOR_KEYS):
                            print(f"Valid data received: {data}")
                            return data
                        else:
                            print(f"Missing keys in data: {data}")
                    except json.JSONDecodeError:
                        print(f"Invalid JSON received: {raw}")
                else:
                    print("Empty response received")
            else:
                print("No data in buffer")
                
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            self.ser.close()
            self.ser = None
            
        return {}

