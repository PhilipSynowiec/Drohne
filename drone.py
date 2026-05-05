from buzzer import Buzzer
from escs import ESCS
from mpu import MPU6050
from time import sleep

class Drone:
    def __init__(self):
        self.buzzer = Buzzer()
        self.mpu = MPU6050()
        self.escs = ESCS()

    def startup(self):
        self.buzzer.start()
        self.buzzer.trigger("startup")
        self.calibrate()
        input("Verninde Batterie und drücke ENTER, um fortzufahren...")
    
    def calibrate(self):
        self.buzzer.trigger("calibration_start")
        sleep(2)
        self.mpu.calibrate()
        self.buzzer.trigger("calibration_done")
        sleep(2)

