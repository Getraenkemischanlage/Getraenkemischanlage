'''
zentrale Konfiguration der Pins und Flussrate

Anschlüsse der Pumpen an den Raspberry Pi:
- Pumpe 1: GP 16
- Pumpe 2: GP 17
- Pumpe 3: GP 20
- Pumpe 4: GP 21

Anschlüsse der Sensoren an den Raspberry Pi:
- DT: GP 1, GP 2, GP 3, GP 4
- SCK: GP 0
- Rot zu E+, Schwarz zu E-, Grün zu A+ und Weiß zu A-
'''

import board
import digitalio
import time
import usb_cdc
import json  # Add this import at the top

# Clock-Pin (gemeinsam für alle Sensoren)
sck = digitalio.DigitalInOut(board.GP0)
sck.direction = digitalio.Direction.OUTPUT

# Datenpins für jede Wägezelle
dout1 = digitalio.DigitalInOut(board.GP1)
dout1.direction = digitalio.Direction.INPUT
dout1.pull = digitalio.Pull.UP

dout2 = digitalio.DigitalInOut(board.GP2)
dout2.direction = digitalio.Direction.INPUT
dout2.pull = digitalio.Pull.UP

dout3 = digitalio.DigitalInOut(board.GP3)
dout3.direction = digitalio.Direction.INPUT
dout3.pull = digitalio.Pull.UP

dout4 = digitalio.DigitalInOut(board.GP4)
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


# Replace the main loop with this debug version:
print("Starting sensor test - waiting for commands...")

while True:
    if usb_cdc.data.in_waiting:
        try:
            cmd = usb_cdc.data.readline().decode().strip()
            print(f"Received command: '{cmd}'")
            
            if cmd == "READ":
                print("Reading sensors...")
                wert1 = hx1.read()
                wert2 = hx2.read()
                wert3 = hx3.read()
                wert4 = hx4.read()
                
                print(f"Raw values: {wert1}, {wert2}, {wert3}, {wert4}")

                data = {
                    "Wasser": wert1,
                    "Sirup_a": wert2,
                    "Sirup_b": wert3,
                    "Sirup_c": wert4
                }
                
                json_data = json.dumps(data) + "\n"
                print(f"Sending: {json_data.strip()}")
                usb_cdc.data.write(json_data.encode())
                usb_cdc.data.flush()
                print("Data sent")
            else:
                print(f"Unknown command: {cmd}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            
    time.sleep(0.1)

'''
while True:
    wert1 = hx1.read()
    wert2 = hx2.read()
    wert3 = hx3.read()
    wert4 = hx4.read()

    daten = f"{wert1},{wert2},{wert3},{wert4}\n"
    usb_cdc.data.write(daten.encode("utf-8"))

    time.sleep(0.5)

# --- Kalibrierdaten (pro Sensor) ---
offset1 = 8320000
faktor1 = 200.0

offset2 = 8315000
faktor2 = 198.5

offset3 = 8321000
faktor3 = 201.2

offset4 = 8318000
faktor4 = 199.0

# --- Sensorwerte mitteln, kalibrieren ---
def lies_sensorwerte():
    # ----------------- Sensor 1 -----------------
    werte1 = []  # Liste für Rohwerte
    for _ in range(5):
        rohwert = hx1.read()       # Rohwert von Sensor 1
        werte1.append(rohwert)
        time.sleep(0.01)           # kurze Pause zwischen den Messungen
    mittel1 = sum(werte1) / 5      # Mittelwert berechnen
    gewicht1 = (mittel1 - offset1) / faktor1  # Umrechnung in Gramm
    gewicht1 = round(gewicht1, 2)  # auf 2 Nachkommastellen runden

    # ----------------- Sensor 2 -----------------
    werte2 = []
    for _ in range(5):
        rohwert = hx2.read()
        werte2.append(rohwert)
        time.sleep(0.01)
    mittel2 = sum(werte2) / 5
    gewicht2 = (mittel2 - offset2) / faktor2
    gewicht2 = round(gewicht2, 2)

    # ----------------- Sensor 3 -----------------
    werte3 = []
    for _ in range(5):
        rohwert = hx3.read()
        werte3.append(rohwert)
        time.sleep(0.01)
    mittel3 = sum(werte3) / 5
    gewicht3 = (mittel3 - offset3) / faktor3
    gewicht3 = round(gewicht3, 2)

    # ----------------- Sensor 4 -----------------
    werte4 = []
    for _ in range(5):
        rohwert = hx4.read()
        werte4.append(rohwert)
        time.sleep(0.01)
    mittel4 = sum(werte4) / 5
    gewicht4 = (mittel4 - offset4) / faktor4
    gewicht4 = round(gewicht4, 2)

    return [gewicht1, gewicht2, gewicht3, gewicht4]

# --- Serielle Kommunikation (USB) ---
print("Warte auf Befehl vom PC...")

# Endlosschleife – wartet immer wieder auf neue Befehle vom Laptop
while True:
    # Prüfen, ob neue Daten über USB empfangen wurden
    if usb_cdc.data.in_waiting:
        # Eine Zeile vom Laptop lesen und in einen String umwandeln
        befehl = usb_cdc.data.readline().decode("utf-8").strip()
        
        # Prüfen, ob der Befehl "READ" lautet
        if befehl == "READ":
            # Sensorwerte auslesen (5x pro Sensor, mitteln, in Gramm umrechnen)
            daten = lies_sensorwerte()

            # Sensorwerte als CSV-Zeile zusammenfügen (z. B. "12.3,0.0,510.2,1.5\n")
            antwort = ",".join(str(w) for w in daten) + "\n"

            # Antwort über USB zurück an den Laptop senden
            usb_cdc.data.write(antwort.encode("utf-8"))
    
    # Kurze Pause, um den Prozessor nicht unnötig zu belasten
    time.sleep(0.1)

















# Pumpe-Klasse
class Pumpe:
    def __init__(self, pin):
        self.relay = pin
        self.relay.direction = digitalio.Direction.OUTPUT
        self.relay.value = False

    def einschalten(self):
        self.relay.value = True

    def ausschalten(self):
        self.relay.value = False

# Pumpen-Instanzen
wasser_pumpe  = Pumpe(digitalio.DigitalInOut(board.GP16))
sirup_a_pumpe = Pumpe(digitalio.DigitalInOut(board.GP17))
sirup_b_pumpe = Pumpe(digitalio.DigitalInOut(board.GP20))
sirup_c_pumpe = Pumpe(digitalio.DigitalInOut(board.GP21))

# Pumpennamen zu Objekten
def pumpe_von_name(name):
    if name == "wasser":
        return wasser_pumpe
    elif name == "sirup_a":
        return sirup_a_pumpe
    elif name == "sirup_b":
        return sirup_b_pumpe
    elif name == "sirup_c":
        return sirup_c_pumpe
    else:
        return None

# Befehlsverarbeitung
def verarbeite_befehl(zeile):
    teile = zeile.strip().lower().split()
    if len(teile) != 2:
        print("Ungültiger Befehl:", zeile)
        return

    name, dauer_str = teile
    pumpe = pumpe_von_name(name)
    if pumpe is None:
        print("Unbekannte Pumpe:", name)
        return

    try:
        dauer = float(dauer_str)
    except ValueError:
        print("Ungültige Dauer:", dauer_str)
        return

    print(f"Pumpe {name} EIN für {dauer} Sekunden")
    pumpe.einschalten()
    time.sleep(dauer)
    pumpe.ausschalten()
    print(f"Pumpe {name} AUS")


# Hauptschleife 
print("Pico bereit für Pumpensteuerung über USB")
while True:
    if usb_cdc.data.in_waiting > 0:
        zeile = usb_cdc.data.readline().decode("utf-8")
        verarbeite_befehl(zeile)
    time.sleep(0.1)









# Konfigurationswerte
totraum = {
    "Wasser":   100,
    "Sirup_a":  100,
    "Sirup_b":  100,
    "Sirup_c":  100,
}

flow_rate = 100       # ml/s
target_volume = 400   # Zielmenge in ml
'''