from time import sleep

from machine import SPI, Pin

from nrf24l01 import NRF24L01

led = Pin("LED", Pin.OUT)

spi = SPI(
    1, baudrate=1_000_000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(11), miso=Pin(12)
)

csn = Pin(13, Pin.OUT, value=1)
ce = Pin(15, Pin.OUT, value=0)

address = b"node1"

nrf = NRF24L01(spi, csn, ce, channel=100, payload_size=1)
nrf.set_power_speed(0x00, 0x20)  # low power, 250 kbps

nrf.open_tx_pipe(address)
nrf.stop_listening()

print("Sender ready")

state = 0

while True:
    state = 1 - state

    try:
        nrf.send(bytes([state]))
        print("sent:", state)
        led.value(state)

    except OSError as e:
        print("send failed:", e)

        # Fehler-Blink
        for _ in range(2):
            led.value(1)
            sleep(0.05)
            led.value(0)
            sleep(0.05)

    sleep(1)
