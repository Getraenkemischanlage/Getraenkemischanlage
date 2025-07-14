
import time
import digitalio

class HX711:
    def __init__(self, dout_pin, sck_pin):
        self.dout = digitalio.DigitalInOut(dout_pin)
        self.dout.direction = digitalio.Direction.INPUT
        self.dout.pull = digitalio.Pull.UP

        self.sck = digitalio.DigitalInOut(sck_pin)
        self.sck.direction = digitalio.Direction.OUTPUT
        self.sck.value = False

    def read(self):
        # Warten bis DOUT auf LOW geht
        while self.dout.value:
            pass

        count = 0
        for _ in range(24):
            self.sck.value = True
            count <<= 1
            self.sck.value = False
            if self.dout.value:
                count += 1

        # 25. Taktimpuls für Gain-Einstellung (z. B. 128)
        self.sck.value = True
        self.sck.value = False

        # Zweierkomplement-Anpassung
        if count & 0x800000:
            count -= 0x1000000

        return count
