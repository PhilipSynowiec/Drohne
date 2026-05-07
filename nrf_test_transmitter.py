from time import sleep

from machine import SPI, Pin

from nrf24l01 import NRF24L01

# Transmitter Pico pins:
# CE   -> GP15
# CSN  -> GP14
# SCK  -> GP10
# MOSI -> GP11
# MISO -> GP12

spi = SPI(
    1, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12)
)

csn = Pin(14, Pin.OUT, value=1)
ce = Pin(15, Pin.OUT, value=0)

nrf = NRF24L01(spi, csn, ce, channel=46, payload_size=1)

address = b"node1"

nrf.open_tx_pipe(address)
nrf.stop_listening()

print("Sender ready")

state = 0

while True:
    state = 1 - state

    try:
        nrf.send(bytes([state]))
        print("sent:", state)
    except OSError as e:
        print("send failed:", e)

    sleep(1)
