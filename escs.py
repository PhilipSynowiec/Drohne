from machine import Pin, PWM
from time import sleep

class ESCS:
    def __init__(self):
        self.escs = [PWM(Pin(pin)) for pin in [12, 13, 14, 15]]
        for esc in self.escs:
            esc.freq(50)

    def set_one(self, us, i):
        esc = self.escs[i]
        esc.duty_ns(us * 1000)
        print(f"ESC{i+1}:", us, "us")
    
    def set_all(self, us):
        for i in range(4):
            self.set_one(us, i)