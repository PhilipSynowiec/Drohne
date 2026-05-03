from machine import Pin, I2C
from time import ticks_us, ticks_diff, sleep
from math import atan2, sqrt, degrees
import struct

MPU_ADDR = 0x68

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

# MPU-6050 aufwecken
i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')

def read_word(reg):
    data = i2c.readfrom_mem(MPU_ADDR, reg, 2)
    return struct.unpack(">h", data)[0]

roll = 0.0   # Grad
pitch = 0.0  # Grad

last_time = ticks_us()
last_print = last_time

while True:
    now = ticks_us()
    dt = ticks_diff(now, last_time) / 1_000_000.0  # Sekunden
    last_time = now

    ax = read_word(0x3B)
    ay = read_word(0x3D)
    az = read_word(0x3F)

    temp_raw = read_word(0x41)

    gx = read_word(0x43)
    gy = read_word(0x45)
    gz = read_word(0x47)

    # Accelerometer in g
    ax_g = ax / 16384.0
    ay_g = ay / 16384.0
    az_g = az / 16384.0

    # Temperatur in °C
    temp_c = (temp_raw / 340.0) + 36.53

    # Gyro in Grad pro Sekunde
    gx_dps = gx / 131.0
    gy_dps = gy / 131.0
    gz_dps = gz / 131.0

    # Accelerometer-Winkel in Grad
    roll_acc = degrees(atan2(ay_g, az_g))
    pitch_acc = degrees(atan2(-ax_g, sqrt(ay_g * ay_g + az_g * az_g)))

    # Complementary Filter, alles in Grad
    roll = 0.98 * (roll + gx_dps * dt) + 0.02 * roll_acc
    pitch = 0.98 * (pitch + gy_dps * dt) + 0.02 * pitch_acc

    if ticks_diff(now, last_print) > 500_000:
        last_print = now
        print("ACC  g   X:{:.2f} Y:{:.2f} Z:{:.2f}".format(ax_g, ay_g, az_g))
        print("GYRO dps X:{:.2f} Y:{:.2f} Z:{:.2f}".format(gx_dps, gy_dps, gz_dps))
        print("TEMP C   {:.2f}".format(temp_c))
        print("ROLL {:.2f} deg  PITCH {:.2f} deg".format(roll, pitch))
        print("-" * 30)

    sleep(0.01)