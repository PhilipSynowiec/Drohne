import struct

from machine import SPI, Pin
from src.nrf24l01 import NRF24L01

FMT_BODY = "<BhhhhBB"
BODY_SIZE = struct.calcsize(FMT_BODY)
PACKET_SIZE = BODY_SIZE + 1


class NRFTransmitter:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        self.spi = SPI(
            1,
            baudrate=2_000_000,
            polarity=0,
            phase=0,
            sck=Pin(14),
            mosi=Pin(11),
            miso=Pin(12),
        )
        self.csn = Pin(13, Pin.OUT, value=1)
        self.ce = Pin(15, Pin.OUT, value=0)
        self.address = b"node1"
        self.nrf = NRF24L01(
            self.spi, self.csn, self.ce, channel=100, payload_size=PACKET_SIZE
        )
        self.nrf.set_power_speed(0x06, 0x20)  # high power, 250 kbps
        self.nrf.open_tx_pipe(self.address)
        self.nrf.stop_listening()
        self.seq = 0
        print("Sender ready")

    def send_state(self, throttle, roll, pitch, yaw, armed, mode):
        body = struct.pack(
            FMT_BODY,
            self.seq,  # uint8
            throttle,  # int16
            roll,  # int16
            pitch,  # int16
            yaw,  # int16
            armed,  # uint8
            mode,  # uint8
        )
        checksum = sum(body) & 0xFF
        packet = body + bytes([checksum])
        self.seq = (self.seq + 1) & 0xFF

        try:
            self.nrf.send(packet)
            print("sent:", (self.seq, throttle, roll, pitch, yaw, armed, mode))
        except OSError as e:
            print("send failed:", e)
