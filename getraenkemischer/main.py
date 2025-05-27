from hardware.sensor_manager import SensorManager
from hardware.pump_controller import PumpController
from logic.drink_suggestion import DrinkSuggestion
from logic.mixer_controller import MixerController

def main():
    # 1. Initialisiere Sensor- und Pumpensteuerung
    sensor_manager = SensorManager()
    pump_controller = PumpController()
    mixer_controller = MixerController(pump_controller)

    # 2. Lese aktuelle Füllstände der Behälter
    fill_levels = {}
    sensor_data = sensor_manager.read_sensors()
    for name, is_full in sensor_data.items():
        fill_levels[name] = 500 if is_full else 0  # z. B. 500 ml wenn voll

    # 3. Erzeuge Vorschlag für mischbares Getränk
    suggestion = DrinkSuggestion(fill_levels)
    best_drink = suggestion.suggest_best_drink()

    if best_drink:
        print(f"\n→ Empfohlenes Getränk: {best_drink}")
        # 4. Mische das Getränk
        mixer_controller.mix(best_drink)
    else:
        print("⚠️ Kein Getränk mischbar. Bitte Behälter auffüllen.")

# Start des Programms
if __name__ == "__main__":
    main()
