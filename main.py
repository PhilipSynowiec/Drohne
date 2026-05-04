from machine import Pin, PWM
from time import sleep

ESC_PIN = 15

MIN_US = 800
MAX_US = 2000

esc = PWM(Pin(ESC_PIN))
esc.freq(50)

def set_esc(us):
    esc.duty_ns(us * 1000)
    print("ESC:", us, "us")

# Sicher starten
set_esc(MIN_US)

print("LiPo anschließen und auf beide Soundgruppen warten.")
sleep(10)

while True:
    raw = input(f"Gaswert {MIN_US}-{MAX_US} eingeben. ENTER = STOP: ").strip()
    value = 800
    # Nur Enter gedrückt
    if not raw == "" and (value >= MIN_US and value <= MAX_US):
        try:
            value = int(raw)
        except ValueError:
            pass
    set_esc(value)