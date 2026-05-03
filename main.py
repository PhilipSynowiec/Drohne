from machine import Pin, PWM
from time import sleep

buzzer = PWM(Pin(16))
buzzer.duty_u16(0)

def tone(freq, duration, duty=22000, pause=0.04):
    buzzer.freq(freq)
    buzzer.duty_u16(duty)
    sleep(duration)
    buzzer.duty_u16(0)
    sleep(pause)

def sound_startup():
    # kurz, aufsteigend: System gestartet
    tone(523, 0.08)    # C5
    tone(659, 0.08)    # E5
    tone(784, 0.08)    # G5
    tone(1047, 0.16)   # C6

def sound_calibration_start():
    # drei gleiche kurze Töne: stillhalten
    tone(440, 0.09)    # A4
    tone(440, 0.09)
    tone(440, 0.09)

def sound_calibration_done():
    # bestätigender Abschluss
    tone(659, 0.08)    # E5
    tone(784, 0.08)    # G5
    tone(988, 0.18)    # B5

# Test
sound_startup()
sleep(1)

sound_calibration_start()
sleep(2)

sound_calibration_done()

buzzer.deinit()