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

# UART Pins für PC Kommunikation
uart_pins = {
    "TX": board.GP12,  # Geändert auf freie Pins
    "RX": board.GP13,  # Geändert auf freie Pins
}

# Totraum je Zutat in ml (realistischere Werte)
totraum = {
    "Wasser": 2,
    "Sirup_a": 1,
    "Sirup_b": 1,
    "Sirup_c": 1,
}

# Flussrate pro Pumpe (ml/s)
flow_rate = 50  # Angepasst auf realistischeren Wert

# Zielmenge (für Mixing z. B. Cocktail)
target_volume = 400

# Minimale und maximale Sensorwerte für Füllstandsberechnung
sensor_limits = {
    "min": 7800000,
    "max": 8600000
}
