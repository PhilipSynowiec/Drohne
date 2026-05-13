from time import sleep, ticks_diff, ticks_ms

from machine import I2C, Pin

from src.ads1x15 import ADS1115
from src.joystick import Joystick
from src.nrf_transmitter import NRFTransmitter

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
ads = ADS1115(i2c, address=0x48, gain=1)

joy1 = Joystick(ads, 0, 1)
joy2 = Joystick(ads, 2, 3)

transmitter = NRFTransmitter()

# joy1.calibrate_full()
# joy2.calibrate_full()

last_print = ticks_ms()
while True:
    now = ticks_ms()
    pitch, roll = joy1.read_value()
    pitch, roll = int(30 * pitch), int(30 * roll)
    throttle, yaw = joy2.read_value()
    throttle, yaw = int(throttle), int(30 * yaw)
    
    transmitter.send_state(throttle, roll, pitch, yaw, armed=1, mode=0)
    sleep(0.02)
