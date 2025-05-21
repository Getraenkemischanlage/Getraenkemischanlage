# gui.py
"""
GUI-Modul für die Getränkemischanlage
Verwendet tkinter, verbindet sich mit MixerController und SensorManager
"""
import threading
import tkinter as tk
from tkinter import ttk

class GUIController:
    def __init__(self, mixer, sensor_manager):
        self.mixer = mixer
        self.sensor_manager = sensor_manager

        self.root = tk.Tk()
        self.root.title("Getränkemischanlage")
        self._build_ui()
        self._update_sensors_loop()

    def _build_ui(self):
        # Getränkewahl
        ttk.Label(self.root, text="Getränk auswählen:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.combo = ttk.Combobox(self.root, values=list(self.mixer.rezepte.keys()), state="readonly")
        self.combo.grid(row=0, column=1, padx=10, pady=5)

        # Buttons
        self.btn_start = ttk.Button(self.root, text="Mischen starten", command=self._on_start)
        self.btn_start.grid(row=1, column=0, padx=10, pady=5)
        self.btn_stop = ttk.Button(self.root, text="Stopp", command=self._on_stop)
        self.btn_stop.grid(row=1, column=1, padx=10, pady=5)

        # Status-Log
        ttk.Label(self.root, text="Status:").grid(row=2, column=0, padx=10, pady=5, sticky='nw')
        self.txt_log = tk.Text(self.root, height=10, width=50, state='disabled')
        self.txt_log.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Sensoranzeige
        frame = ttk.LabelFrame(self.root, text="Sensorwerte")
        frame.grid(row=0, column=2, rowspan=4, padx=10, pady=5, sticky='ns')
        self.lbl_level = ttk.Label(frame, text="Füllstände: --")
        self.lbl_level.pack(anchor='w', padx=5, pady=2)
        self.lbl_temp = ttk.Label(frame, text="Temperatur: -- °C")
        self.lbl_temp.pack(anchor='w', padx=5, pady=2)

    def _on_start(self):
        rezept = self.combo.get()
        if not rezept:
            self._log("⚠ Bitte Getränk auswählen!")
            return
        self._log(f"🔄 Starte Mischung: {rezept}")
        threading.Thread(target=self._run_mix, args=(rezept,), daemon=True).start()

    def _on_stop(self):
        # Stop-Logik evtl. implementieren
        self._log("⛔ Stop ausgelöst")

    def _run_mix(self, rezept):
        self.mixer.mix(rezept, log_callback=self._log)

    def _log(self, text):
        self.txt_log.configure(state='normal')
        self.txt_log.insert('end', text + "\n")
        self.txt_log.configure(state='disabled')
        self.txt_log.see('end')

    def _update_sensors_loop(self):
        levels = self.sensor_manager.lese_level()
        temps = self.sensor_manager.lese_temp()
        lvl_str = ", ".join(f"{name}:{'voll' if val else 'leer'}" for name, val in levels.items())
        tmp_str = ", ".join(f"{name}:{val:.1f}°C" for name, val in temps.items())
        self.lbl_level.config(text="Füllstände: " + lvl_str)
        self.lbl_temp.config(text="Temperatur: " + tmp_str)
        self.root.after(1000, self._update_sensors_loop)

    def run(self):
        self.root.mainloop()

# Beispielaufruf
if __name__ == '__main__':
    # Diese Objekte müssen entsprechend importiert und instanziiert werden
    from mixer_controller.mixer_controller import MixerController
    from hardware import SensorManager
    
    # Dummy-Initialisierung
    mixer = MixerController(pumpen={})
    sensor_mgr = SensorManager(level_sensors={}, temp_sensors={})
    
    gui = GUIController(mixer, sensor_mgr)
    gui.run()
