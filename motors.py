from machine import Pin, PWM
from time import sleep
from pid import PID

PIN_FL = 12
PIN_FR = 13
PIN_BL = 14
PIN_BR = 15

class Motor:
    def __init__(self, pin):
        self.pin = pin
        self.esc = PWM(Pin(pin))
        self.esc.freq(50)

    def set(self, us):
        us = max(800, min(2000, us))  # Signal begrenzen
        self.esc.duty_ns(us * 1000)
        print(f"Motor on pin {self.pin}:", us, "us")

class MotorController:
    def __init__(self):
        self.roll_pid = PID(kp=2.0, ki=0.0, kd=0.0, output_min=-150, output_max=150, integral_limit=80)
        self.pitch_pid = PID(kp=2.0, ki=0.0, kd=0.0, output_min=-150, output_max=150, integral_limit=80)
        self.yaw_pid = PID(kp=1.0, ki=0.0, kd=0.0, output_min=-100, output_max=100, integral_limit=50)
        self.motor_fl = Motor(PIN_FL)
        self.motor_fr = Motor(PIN_FR)
        self.motor_bl = Motor(PIN_BL)
        self.motor_br = Motor(PIN_BR)
    
    def update(self, desired_roll, desired_pitch, desired_yaw, current_roll, current_pitch, current_yaw, dt):
        roll_output = self.roll_pid.update(desired_roll, current_roll, dt)
        pitch_output = self.pitch_pid.update(desired_pitch, current_pitch, dt)
        yaw_output = self.yaw_pid.update(desired_yaw, current_yaw, dt)

        base_throttle = 1500  # Basis-Drehzahl in us

        # Motor-Signale berechnen
        fl_signal = base_throttle + roll_output + pitch_output - yaw_output
        fr_signal = base_throttle - roll_output + pitch_output + yaw_output
        bl_signal = base_throttle + roll_output - pitch_output + yaw_output
        br_signal = base_throttle - roll_output - pitch_output - yaw_output

        # Motoren ansteuern
        self.motor_fl.set(fl_signal)
        self.motor_fr.set(fr_signal)
        self.motor_bl.set(bl_signal)
        self.motor_br.set(br_signal)