from time import sleep, ticks_diff, ticks_ms

from src.nrf_receiver import NRFReceiver

receiver = NRFReceiver()

last_print = ticks_ms()
while True:
    now = ticks_ms()

    state = receiver.receive_state()
    if state is not None:
        throttle, roll, pitch, yaw, armed, mode = state
    if ticks_diff(now, last_print) >= 500:
        if state is not None:
            print(f"pitch={pitch:.2f}, roll={roll:.2f}")
            print(f"throttle={throttle:.2f}, yaw={yaw:.2f}\n")
        else:
            print("no data received\n")
        last_print = now
        receiver.led.toggle()
    sleep(0.01)
