import tkinter as tk
from gui import BeverageGUI

import serial
import time

# COM-Port deines Pico (anpassen falls nötig, z. B. "COM3" oder "/dev/ttyACM0")
COM_PORT = "COM5"
BAUDRATE = 9600

def sende_befehl(ser, befehl):
    befehl = befehl.strip() + "\n"
    ser.write(befehl.encode("utf-8"))

    # Wenn "READ" gesendet wurde, Antwort lesen
    if befehl.strip().upper() == "READ":
        antwort = ser.readline().decode("utf-8").strip()
        try:
            werte = [float(w) for w in antwort.split(",")]
            print("Sensorwerte (g):", werte)
        except ValueError:
            print("Fehlerhafte Antwort:", antwort)
    else:
        print("Befehl gesendet:", befehl.strip())

def main():
    try:
        ser = serial.Serial(COM_PORT, BAUDRATE, timeout=2)
        time.sleep(2)  # Zeit geben, damit der Pico starten kann

        print("Verbindung zum Pico hergestellt.")
        print("Befehle:")
        print(" - READ               → Sensoren abfragen")
        print(" - wasser 1.5         → Wasserpumpe 1.5 Sek. einschalten")
        print(" - sirup_a 2          → Sirup-A-Pumpe 2 Sek. einschalten")
        print(" - quit               → Beenden")

        while True:
            befehl = input(">>> ").strip()
            if befehl.lower() == "quit":
                break
            sende_befehl(ser, befehl)

        ser.close()
        print("Verbindung geschlossen.")

    except serial.SerialException as e:
        print("Fehler beim Öffnen des COM-Ports:", e)

if __name__ == "__main__":
    main()



'''
ser = serial.Serial('COM5', 9600)  # COM-Port ggf. anpassen
time.sleep(2)  # Warten, bis Pico bereit ist

# Pumpe "wasser" für 3 Sekunden einschalten
ser.write(b"wasser 3\n")


def main():
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

'''