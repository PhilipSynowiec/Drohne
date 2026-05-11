from time import sleep, ticks_diff, ticks_ms

from src.joystick import Joystick

pitch_roll = Joystick(26, 27)
throttle_yaw = Joystick(20, 21)

last_print = 0
while True:
    now = ticks_ms()
    pitch, roll = pitch_roll.read_value()
    throttle, yaw = throttle_yaw.read_value()

    if ticks_diff(now, last_print) >= 100:
        print(f"pitch={pitch:.2f}, roll={roll:.2f}")
        print(f"throttle={throttle:.2f}, yaw={yaw:.2f}\n")
        last_print = now
    sleep(0.01)
