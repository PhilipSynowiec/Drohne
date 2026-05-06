from time import sleep

from machine import SPI, Pin

from nrf24l01 import NRF24L01

led = Pin("LED", Pin.OUT)

# nRF24:
# MISO -> GP0
# CSN  -> GP1
# SCK  -> GP2
# MOSI -> GP3
# CE   -> GP4
spi = SPI(
    0, baudrate=500_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(0)
)

csn = Pin(1, Pin.OUT, value=1)
ce = Pin(4, Pin.OUT, value=0)

print("nRF24 Hardware-Test startet...")

while True:
    try:
        nrf = NRF24L01(spi, csn, ce, channel=46, payload_size=1)
        print("OK: nRF24 antwortet")
        led.value(1)
        sleep(1)

    except OSError as e:
        print("FEHLER:", e)
        led.value(0)
        sleep(1)
