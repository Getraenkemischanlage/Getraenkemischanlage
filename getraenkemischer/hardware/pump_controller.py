'''
Funktion:
- Ordnet die Pumpen Pins zu und setzt sie als Ausgang
- Steuert die Pumpen an 

Klassen: 
- PumpController
    Klassenobjekte:
    - pump_pins: dict
    - flow_rate_ml_per_sec: float
    - pumps: dict
    Klassenmethoden:
    - __init__()
    - dispense(ingredient: str, amount_ml: float)


'''
from config import PUMP_PINS, FLOW_RATE

class PumpController:
    def __init__(self):       
        self.pump_pins = PUMP_PINS  # Zuordnung der Pumpen zu den Pins

        self.flow_rate_ml_per_sec = FLOW_RATE  # Durchflussrate: z. B. 10 ml/s

        self.pumps = {} # Dictionary mit Pumpen der verschiedenen Behältern und zugeordneten Pins


    