
import board
import digitalio
import time
import json

# Clock-Pin (gemeinsam für alle Sensoren)
sck = digitalio.DigitalInOut(board.GP0)
sck.direction = digitalio.Direction.OUTPUT

# Datenpins für jede Wägezelle
dout1 = digitalio.DigitalInOut(board.GP1)  # Wasser
dout1.direction = digitalio.Direction.INPUT
dout1.pull = digitalio.Pull.UP

dout2 = digitalio.DigitalInOut(board.GP2)  # Sirup_a
dout2.direction = digitalio.Direction.INPUT
dout2.pull = digitalio.Pull.UP

dout3 = digitalio.DigitalInOut(board.GP3)  # Sirup_b
dout3.direction = digitalio.Direction.INPUT
dout3.pull = digitalio.Pull.UP

dout4 = digitalio.DigitalInOut(board.GP4)  # Sirup_c
dout4.direction = digitalio.Direction.INPUT
dout4.pull = digitalio.Pull.UP


class HX711:
    def __init__(self, dout_pin, sck_pin):
        self.dout = dout_pin
        self.pd_sck = sck_pin
        self.pd_sck.value = False

    def read(self):
        while self.dout.value:
            pass

        count = 0
        for _ in range(24):
            self.pd_sck.value = True
            count = count << 1
            self.pd_sck.value = False
            if self.dout.value:
                count += 1

        self.pd_sck.value = True
        count = count ^ 0x800000
        self.pd_sck.value = False

        return count


# Vier HX711-Instanzen mit gemeinsamen SCK, aber je eigenem DOUT
hx1 = HX711(dout_pin=dout1, sck_pin=sck)
hx2 = HX711(dout_pin=dout2, sck_pin=sck)
hx3 = HX711(dout_pin=dout3, sck_pin=sck)
hx4 = HX711(dout_pin=dout4, sck_pin=sck)

# Sensor names matching the PC configuration
SENSOR_NAMES = ["Wasser", "Sirup_a", "Sirup_b", "Sirup_c"]
sensors = [hx1, hx2, hx3, hx4]

def read_all_sensors():
    """Read all sensors and return as dictionary with proper names"""
    results = {}
    for i, sensor in enumerate(sensors):
        try:
            value = sensor.read()
            results[SENSOR_NAMES[i]] = value
        except Exception as e:
            results[SENSOR_NAMES[i]] = 0
    return results

# Main loop - continuously send sensor data
while True:
    try:
        # Read all sensors
        sensor_data = read_all_sensors()
        
        # Send JSON data via print (which goes to console/serial)
        json_response = json.dumps(sensor_data)
        print(f"JSON_DATA:{json_response}")
        
        # Also print human-readable format for debugging
        print(f"Sensor 1: {sensor_data['Wasser']} | Sensor 2: {sensor_data['Sirup_a']} | Sensor 3: {sensor_data['Sirup_b']} | Sensor 4: {sensor_data['Sirup_c']}")
        
        time.sleep(1.0)  # Send data every second
        
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(1)
