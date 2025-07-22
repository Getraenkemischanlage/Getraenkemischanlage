'''import serial
import json

class PicoSerialInterface:
    def __init__(self, port="/dev/ttyACM0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=2)

    def send_command(self, cmd):
        self.ser.write((cmd + "\n").encode())

    def read_response(self):
        return self.ser.readline().decode().strip()

    def get_fill_levels(self):
        self.send_command("READ_FILL_LEVELS")
        response = self.read_response()
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {}

    def dispense(self, ingredient, amount_ml):
        self.send_command(f"DISPENSE {ingredient} {amount_ml}")
        return self.read_response()

    def emergency_stop(self):
        self.send_command("EMERGENCY_STOP")
        return self.read_response()

    def reset_pumps(self):
        self.send_command("RESET_PUMPS")
        return self.read_response()
        '''
