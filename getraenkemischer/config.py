# code_config.py

# Zutaten-Namen (müssen mit sensor- und pumpen-Namen auf dem Pico übereinstimmen)
INGREDIENTS = ["Wasser", "Sirup_a", "Sirup_b", "Sirup_c"]

# Totraum je Zutat – verwendet in GUI zur Abschätzung, falls nötig
totraum = {
    "Wasser": 100,
    "Sirup_a": 100,
    "Sirup_b": 100,
    "Sirup_c": 100,
}

# Förderrate pro Pumpe (zum Anzeigen evtl. zusätzlich in GUI genutzt)
flow_rate = 100.0  # ml/s

# Zielmenge für die GUI-Logik (z. B. bei empfohlenem Getränk)
target_volume = 400

# Serial Port Einstellungen (kann in GUI angepasst werden)
SERIAL_PORT = "/dev/ttyACM0"  # oder "COM5" auf Windows
BAUDRATE = 115200
