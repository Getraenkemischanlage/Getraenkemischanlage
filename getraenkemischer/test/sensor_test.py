from hardware.sensor_manager import SensorManager
import time

sm = SensorManager()
while True:
    print(sm.read_sensors())
    time.sleep(1)
