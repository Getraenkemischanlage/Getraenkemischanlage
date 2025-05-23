'''
Funktion:
- Ordnet die Pumpen zu Pins zu und setzt sie als Ausgang
- Steuert die Pumpen an 

Methoden:
- dispense (bekommt, ingridient und amount_ml)

Anschlüsse der Pumpen an den Raspberry Pi:
- Pumpe 1: GP 22
- Pumpe 2: GP 21
- Pumpe 3: GP 20
- Pumpe 4: GP 19
- Pumpe 5: GP 18

'''
from machine import Pin
from neopixel import NeoPixel #für Testlauf mit LEDs
import time

class PumpController:
    def __init__(self):       
        # Zuordnung der Pumpen zu den Pins
        self.pump_pins = {
            "Wasser": 1,     
            "Sirup_a": 21,    
            "Sirup_b": 20,    
            "Sirup_c": 19,
            "Alkohol": 18     
        }

        self.flow_rate_ml_per_sec = 10  # Durchflussrate: z. B. 10 ml/s

        self.pumps = {}                 # Dictionary mit Pumpen der verschiedenen Behältern und zugeordneten Pins

        
        #Initialisiert alle Pumpen-Pins als Ausgang
        for name, pin_number in self.pump_pins.items():
            self.pumps[name] = Pin(pin_number, Pin.OUT)


    def dispense(self, ingredient, amount_ml):
        #Jeweilige Pumpe wird so lange angesteuert bis gewünschte Menge erreicht ist
        #Bekommt ingridient (Welche Flüssigkeit soll gefördert werden?) und amount_ml (Welche Menge) übermittelt

        #Überprüfung ob für Zutat eine Pumpe vorhanden ist
        if ingredient not in self.pumps:
            print(f"Zutat '{ingredient}' ist keiner Pumpe zugewiesen.")
            return

        #Berechnung der Förderzeit
        duration = amount_ml / self.flow_rate_ml_per_sec
        
        #Auswahl der richtigen Pumpe
        pump = self.pumps[ingredient]

        #Ausgabe für Benutzer
        print(f"Zutat {ingredient}: {amount_ml} ml ausgeben ({duration:.2f} Sekunden)")

        #Pumpe aktivieren
        pump.value(1)
        time.sleep(duration)
        pump.value(0)