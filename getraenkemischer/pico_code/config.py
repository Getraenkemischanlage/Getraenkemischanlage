import board

# Pin-Zuordnung für Pumpen
pump_pins = {
    "Wasser": board.GP16,
    "Sirup_a": board.GP17,
    "Sirup_b": board.GP18,
    "Sirup_c": board.GP19,
}

# Pin-Zuordnung für HX711-Sensoren
sensor_pins = {
    "SCK": board.GP0,         # gemeinsamer Clock-Pin
    "Wasser": board.GP1,
    "Sirup_a": board.GP2,
    "Sirup_b": board.GP3,
    "Sirup_c": board.GP4,
}

# Totraum je Zutat (ml)
totraum = {
    "Wasser": 100,
    "Sirup_a": 100,
    "Sirup_b": 100,
    "Sirup_c": 100,
}

# Flussrate pro Pumpe (ml/s)
flow_rate = 100

# Zielmenge (für Mixing z. B. Cocktail)
target_volume = 400
