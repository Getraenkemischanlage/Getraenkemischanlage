import time
from config import pump_pins, totraum, flow_rate
import digitalio
import board
import busio
import json

class PumpController:
    def __init__(self):
        self.flow_rate_ml_per_sec = flow_rate
        self.totraum = totraum
        self.is_emergency = False

        # Initialize UART for PC communication
        self.uart = busio.UART(tx=board.GP0, rx=board.GP1, baudrate=9600)

        # Initialize pumps
        self.pumps = {}
        for name, pin in pump_pins.items():
            p = digitalio.DigitalInOut(pin)
            p.direction = digitalio.Direction.OUTPUT
            p.value = False
            self.pumps[name] = p

    def dispense(self, ingredient, amount_ml):
        if self.is_emergency:
            self.send_message(f"Emergency stop active - cannot dispense {ingredient}")
            return False

        if ingredient not in self.pumps:
            self.send_message(f"Unknown pump: {ingredient}")
            return False

        pump = self.pumps[ingredient]
        duration = amount_ml / self.flow_rate_ml_per_sec
        duration_totraum = self.totraum.get(ingredient, 0) / self.flow_rate_ml_per_sec

        try:
            # Start pump
            pump.value = True
            time.sleep(duration_totraum + duration)
            pump.value = False
            self.send_message(f"Dispensed {amount_ml}ml of {ingredient}")
            return True
        except Exception as e:
            self.send_message(f"Error dispensing {ingredient}: {str(e)}")
            pump.value = False
            return False

    def emergency_stop(self):
        self.is_emergency = True
        for pump in self.pumps.values():
            pump.value = False
        self.send_message("Emergency stop activated")

    def reset_pumps(self):
        self.is_emergency = False
        for pump in self.pumps.values():
            pump.value = False
        self.send_message("Pumps reset")

    def send_message(self, message):
        try:
            self.uart.write(f"{message}\n".encode())
        except Exception as e:
            print(f"UART error: {e}")

    def process_command(self, command):
        try:
            if command == "STOP":
                self.emergency_stop()
                return
                
            if command == "RESET":
                self.reset_pumps()
                return
                
            # Parse recipe command: {"ingredient": amount_ml, ...}
            recipe = json.loads(command)
            for ingredient, amount in recipe.items():
                if not self.dispense(ingredient, float(amount)):
                    return
            
            self.send_message("Recipe completed")
            
        except Exception as e:
            self.send_message(f"Command error: {str(e)}")
            self.emergency_stop()

    def run(self):
        while True:
            if self.uart.in_waiting:
                try:
                    command = self.uart.readline().decode().strip()
                    if command:
                        self.process_command(command)
                except Exception as e:
                    print(f"Error reading command: {e}")
                    self.emergency_stop()
            time.sleep(0.1)

# Start controller when file is run
if __name__ == "__main__":
    controller = PumpController()
    controller.run()
