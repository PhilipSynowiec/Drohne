from machine import Pin, I2C
from time import ticks_us, ticks_diff, sleep
from math import atan2, sqrt, degrees
import struct

class MPU6050:
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
        self.addr = 0x68
        # MPU-6050 aufwecken
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
        self.roll = 0.0
        self.pitch = 0.0
        self.last_time = ticks_us()
        self.last_print = self.last_time

    def read_word(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        return struct.unpack(">h", data)[0]
    
    def calibrate(self):
        print("Kalibriere MPU-6050... Bitte stillhalten!")
        ax_offset = 0
        ay_offset = 0
        az_offset = 0
        gx_offset = 0
        gy_offset = 0
        gz_offset = 0
        samples = 100

        for _ in range(samples):
            ax_offset += self.read_word(0x3B)
            ay_offset += self.read_word(0x3D)
            az_offset += self.read_word(0x3F)
            gx_offset += self.read_word(0x43)
            gy_offset += self.read_word(0x45)
            gz_offset += self.read_word(0x47)
            sleep(0.01)

        self.ax_offset = ax_offset / samples
        self.ay_offset = ay_offset / samples
        self.az_offset = az_offset / samples
        self.gx_offset = gx_offset / samples
        self.gy_offset = gy_offset / samples
        self.gz_offset = gz_offset / samples

        print("Kalibrierung abgeschlossen.")
        print("Offsets: ax={:.2f} ay={:.2f} az={:.2f} gx={:.2f} gy={:.2f} gz={:.2f}".format(
            self.ax_offset, self.ay_offset, self.az_offset, self.gx_offset, self.gy_offset, self.gz_offset))


    def fetch_data(self):
        now = ticks_us()
        dt = ticks_diff(now, self.last_time) / 1_000_000.0  # Sekunden
        self.last_time = now

        ax = self.read_word(0x3B) - self.ax_offset
        ay = self.read_word(0x3D) - self.ay_offset
        az = self.read_word(0x3F) - self.az_offset

        temp_raw = self.read_word(0x41)

        gx = self.read_word(0x43) - self.gx_offset
        gy = self.read_word(0x45) - self.gy_offset
        gz = self.read_word(0x47) - self.gz_offset

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
        self.roll = 0.98 * (self.roll + gx_dps * dt) + 0.02 * roll_acc
        self.pitch = 0.98 * (self.pitch + gy_dps * dt) + 0.02 * pitch_acc

        if ticks_diff(now, self.last_print) > 500_000:
            self.last_print = now
            print("ACC  g   X:{:.2f} Y:{:.2f} Z:{:.2f}".format(ax_g, ay_g, az_g))
            print("GYRO dps X:{:.2f} Y:{:.2f} Z:{:.2f}".format(gx_dps, gy_dps, gz_dps))
            print("TEMP C   {:.2f}".format(temp_c))
            print("ROLL {:.2f} deg  PITCH {:.2f} deg".format(self.roll, self.pitch))
            print("-" * 30)

        return self.roll, self.pitch, temp_c