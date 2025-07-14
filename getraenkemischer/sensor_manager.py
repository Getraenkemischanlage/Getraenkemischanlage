import time

# Vereinfachter HX711-Treiber für Pico
class HX711:
    def __init__(self, dout, pd_sck):
        self.dout = Pin(dout, Pin.IN, pull=Pin.PULL_UP)
        self.pd_sck = Pin(pd_sck, Pin.OUT)
        self.pd_sck.value(0)

    def read(self):
        # Warten bis Daten bereit (DOUT = LOW)
        while self.dout.value() == 1:
            pass

        count = 0
        for _ in range(24):
            self.pd_sck.value(1)
            count = count << 1
            self.pd_sck.value(0)
            if self.dout.value():
                count += 1

        # 25. Taktimpuls für Kanal-/Verstärkungseinstellung
        self.pd_sck.value(1)
        count = count ^ 0x800000  # Zweierkomplement-Anpassung
        self.pd_sck.value(0)

        return count


class SensorManager:
    def __init__(self):
        self.ser = None

    def read_fill_levels(self):
        try:
            with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2) as ser:
                ser.write(b"READ\n")  # Sende Befehl an den Pico
                raw = ser.readline().decode().strip()
                if raw:
                    data = json.loads(raw)
                    return data
                else:
                    print("Keine Daten empfangen.")
                    return {}
        except Exception as e:
            print(f"[SensorManager] Fehler bei der Verbindung: {e}")
            return {}
