from sensor_manager import SensorManager
from pump_controller import PumpController
import tkinter as tk
from gui import BeverageGUI

def main():
    # 1. Initialisiere Sensor- und Pumpensteuerung
    sensor_manager = SensorManager()
    pump_controller = PumpController()

    # 2. Lese aktuelle Füllstände der Behälter
    fill_levels = {}
    sensor_data = sensor_manager.read_fill_levels()  # Lese Füllstände von Sensoren
    for name, is_full in sensor_data.items():
        fill_levels[name] = 500 if is_full else 0  # z. B. 500 ml wenn voll


# Start des Programms
if __name__ == "__main__":
    root = tk.Tk()
    app = BeverageGUI(root)
    root.mainloop()

