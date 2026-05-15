import struct

from machine import SPI, Pin

from src.nrf24l01 import NRF24L01

FMT_BODY = "<BhhhhBB"
BODY_SIZE = struct.calcsize(FMT_BODY)
PACKET_SIZE = BODY_SIZE + 1


class NRFReceiver:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        self.spi = SPI(
            0,
            baudrate=2_000_000,
            polarity=0,
            phase=0,
            sck=Pin(2),
            mosi=Pin(3),
            miso=Pin(0),
        )
        self.csn = Pin(1, Pin.OUT, value=1)
        self.ce = Pin(6, Pin.OUT, value=0)
        self.address = b"node1"
        self.nrf = NRF24L01(
            self.spi, self.csn, self.ce, channel=76, payload_size=PACKET_SIZE
        )
        self.nrf.set_power_speed(0x06, 0x20)  # high power, 250 kbps
        self.nrf.open_rx_pipe(1, self.address)
        self.nrf.start_listening()
        print("Receiver ready")

    def receive_state(self):
        if self.nrf.any():
            packet = self.nrf.recv()
            if len(packet) != PACKET_SIZE:
                print("invalid packet size:", len(packet))
                return None
            body = packet[:-1]
            checksum = packet[-1]
            if sum(body) & 0xFF != checksum:
                print("checksum error")
                return None
            seq, throttle, roll, pitch, yaw, armed, mode = struct.unpack(FMT_BODY, body)
            print("received:", (seq, throttle, roll, pitch, yaw, armed, mode))
            return throttle, roll, pitch, yaw, armed, mode
