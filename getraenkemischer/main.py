from hardware.sensor_manager import SensorManager
from hardware.pump_controller import PumpController
from getraenkemischer.algorithm.mixer_controller import MixerController
import tkinter as tk
from gui.gui import BeverageGUI

def main():
    # 0. Test Pumpensteuerung 
    pump_controller = PumpController()
    pump_controller.dispense("Wasser", 100)  # Beispiel: 100 ml Wasser ausgeben


    # 1. Initialisiere Sensor- und Pumpensteuerung
    sensor_manager = SensorManager()
    pump_controller = PumpController()
    mixer_controller = MixerController(pump_controller)

    # 2. Lese aktuelle Füllstände der Behälter
    fill_levels = {}
    sensor_data = sensor_manager.read_sensors()
    for name, is_full in sensor_data.items():
        fill_levels[name] = 500 if is_full else 0  # z. B. 500 ml wenn voll

# Start des Programms
if __name__ == "__main__":
    root = tk.Tk()
    app = BeverageGUI(root)
    root.mainloop()

