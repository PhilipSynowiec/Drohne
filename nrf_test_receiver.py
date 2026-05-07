from time import sleep

from machine import SPI, Pin

from nrf24l01 import NRF24L01

led = Pin("LED", Pin.OUT)

spi = SPI(
    0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(0)
)

csn = Pin(1, Pin.OUT, value=1)
ce = Pin(6, Pin.OUT, value=0)

nrf = NRF24L01(spi, csn, ce, channel=46, payload_size=1)

address = b"node1"

nrf.open_rx_pipe(1, address)
nrf.start_listening()

print("Receiver ready")

while True:
    if nrf.any():
        data = nrf.recv()
        value = data[0]

        print("received:", value)

        if value == 1:
            led.value(1)
        elif value == 0:
            led.value(0)

    sleep(0.01)
