from time import sleep

from machine import SPI, Pin

from src.nrf24l01 import NRF24L01

led = Pin("LED", Pin.OUT)

spi = SPI(
    0, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(0)
)

csn = Pin(1, Pin.OUT, value=1)
ce = Pin(6, Pin.OUT, value=0)

address = b"node1"

nrf = NRF24L01(spi, csn, ce, channel=100, payload_size=1)
nrf.set_power_speed(0x00, 0x20)  # low power, 250 kbps

nrf.open_rx_pipe(1, address)
nrf.start_listening()

print("Receiver ready")

for _ in range(3):
    led.value(1)
    sleep(0.15)
    led.value(0)
    sleep(0.15)

while True:
    if nrf.any():
        data = nrf.recv()
        value = data[0]

        print("received:", value)
        led.value(value)

    sleep(0.01)
