from machine import Pin, PWM
from utime import sleep
from neopixel import NeoPixel

# Anschluss der LED
ledPin = 1
ledCount = 4

# Initialisiere GPIOs
led = Pin(ledPin, Pin.OUT)
led = NeoPixel(Pin(ledPin, Pin.OUT), ledCount)

# Farbe
led[0] = (255, 255, 255)
led[1] = (0, 0, 0)
led[2] = (0, 0, 0)
led[3] = (0, 0, 0)

# LED anschalten
led.write()
sleep(1)




while True:
    # Turn LEDs white
    for i in range (ledCount):
        led[i] = (255, 255, 255)
        led.write()
        sleep(1)
    # Turn LEDs red
    for i in range (ledCount):
        led[i] = (255, 0, 0)
        led.write()
        sleep(1)
    # Turn LEDs blue
    for i in range (ledCount):
        led[i] = (0, 0, 255)
        led.write()
        sleep(1)
    # Turn LEDs green
    for i in range (ledCount):
        led[i] = (0, 255, 0)
        led.write()
        sleep(1)
        