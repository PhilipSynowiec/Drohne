from machine import Pin, PWM
from time import sleep

ESC_PINS = [12, 13, 14, 15]

MIN_US = 800
MAX_US = 2000

escs = [PWM(Pin(pin)) for pin in ESC_PINS]
for esc in escs:
    esc.freq(50)

def set_escs(us, i=None):
    if i is None:
        for esc in escs:
            esc.duty_ns(us * 1000)
    else:
        escs[i].duty_ns(us * 1000)

    print("Signal ESCs:", us, "us")

def stop_forever():
    print("STOP: halte 800 us dauerhaft.")
    print("Danach LiPo abziehen.")
    while True:
        for esc in escs:
            esc.duty_ns(MIN_US * 1000)
        sleep(0.02)

# Sicheres Startsignal
set_escs(MIN_US)

print("LiPo an ESCs anschließen und auf Starttöne warten.")
sleep(8)

while True:
    raw = input("Signal in us eingeben 800-2000, ENTER = STOP: ").strip()

    if raw == "":
        stop_forever()

    try:
        us = int(raw)
    except ValueError:
        stop_forever()

    if us < MIN_US or us > MAX_US:
        stop_forever()

    set_escs(us)