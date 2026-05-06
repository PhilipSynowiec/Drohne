import _thread
from time import sleep

from machine import PWM, Pin


class Buzzer:
    def __init__(self, pin_num=16):
        self.buzzer = PWM(Pin(pin_num))
        self.buzzer.duty_u16(0)

        self.lock = _thread.allocate_lock()
        self.queue = []
        self.thread_running = False

    def tone(self, freq, duration, duty=22000, pause=0.04):
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(duty)

        sleep(duration)

        self.buzzer.duty_u16(0)
        sleep(pause)

    def sound_startup(self):
        # kurz, aufsteigend: System gestartet
        self.tone(523, 0.08)  # C5
        self.tone(659, 0.08)  # E5
        self.tone(784, 0.08)  # G5
        self.tone(1047, 0.16)  # C6

    def sound_calibration_start(self):
        # drei gleiche kurze Töne: stillhalten
        self.tone(440, 0.09)  # A4
        self.tone(440, 0.09)
        self.tone(440, 0.09)

    def sound_calibration_done(self):
        # bestätigender Abschluss
        self.tone(659, 0.08)  # E5
        self.tone(784, 0.08)  # G5
        self.tone(988, 0.18)  # B5

    def play_sound(self, sound_name):
        if sound_name == "startup":
            self.sound_startup()

        elif sound_name == "calibration_start":
            self.sound_calibration_start()

        elif sound_name == "calibration_done":
            self.sound_calibration_done()

    def sound_worker(self):
        while True:
            sound_to_play = None

            with self.lock:
                if len(self.queue) > 0:
                    sound_to_play = self.queue.pop(0)

            if sound_to_play is not None:
                self.play_sound(sound_to_play)

            sleep(0.01)

    def start(self):
        with self.lock:
            if self.thread_running:
                return

            self.thread_running = True

        _thread.start_new_thread(self.sound_worker, ())

    def trigger(self, sound_name):
        with self.lock:
            self.queue.append(sound_name)

    def deinit(self):
        self.buzzer.duty_u16(0)
        self.buzzer.deinit()
