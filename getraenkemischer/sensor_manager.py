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
            print("Reading sensor data...")
            
            # Wait for data to be available
            timeout_counter = 0
            while not self.ser.in_waiting and timeout_counter < 50:  # 5 second timeout
                time.sleep(0.1)
                timeout_counter += 1
            
            if not self.ser.in_waiting:
                print("No data received within timeout")
                return {}
            
            # Read multiple lines to find valid JSON
            responses = []
            for _ in range(5):  # Read up to 5 lines
                if self.ser.in_waiting:
                    line = self.ser.readline().decode().strip()
                    if line:
                        responses.append(line)
                        print(f"Raw data received: {line}")
                else:
                    break
            
            # Look for a valid JSON response among all lines received
            for raw in responses:
                if raw and raw.startswith('JSON_DATA:'):  # Look for JSON data prefix
                    json_part = raw[10:]  # Remove "JSON_DATA:" prefix
                    try:
                        data = json.loads(json_part)
                        if all(key in data for key in SENSOR_KEYS):
                            print(f"Valid data received: {data}")
                            return data
                        else:
                            print(f"Missing keys in data: {data}")
                    except json.JSONDecodeError:
                        print(f"Invalid JSON received: {json_part}")
            
            if not responses:
                print("No response received")
                
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            self.ser.close()
            self.ser = None
            
        return {}

