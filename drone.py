from buzzer import Buzzer
from motors import MotorController
from mpu import MPU6050
from time import sleep, ticks_us, ticks_diff
from state import State


class Drone:
    def __init__(self):
        self.buzzer = Buzzer()
        self.mpu = MPU6050()
        self.motors = MotorController()

    def startup(self):
        self.buzzer.start()
        self.buzzer.trigger("startup")
        self.calibrate()
        input("Verbinde Batterie und drücke ENTER, um fortzufahren...")

    def calibrate(self):
        self.buzzer.trigger("calibration_start")
        sleep(2)
        self.mpu.calibrate()
        self.buzzer.trigger("calibration_done")
        sleep(2)

    def update(self, dt):
        (roll, pitch, yaw) = self.mpu.read(dt)
        state = State(roll, pitch, yaw)
        desired_state = State(
            roll=0.0, pitch=0.0, yaw=0.0
        )  # TODO: read from remote control
        self.motors.update(desired_state, state, dt)

    def main_loop(self):
        last_time = ticks_us()
        while True:
            now = ticks_us()
            dt = ticks_diff(now, last_time) / 1_000_000.0  # Sekunden
            last_time = now
            self.update(dt)
            sleep(0.02)
