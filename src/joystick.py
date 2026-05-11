import time

MAX_INT = 32767


def normalize(value):
    return value / MAX_INT


class Joystick:
    def __init__(
        self,
        ads,
        vrx_channel,
        vry_channel,
        deadzone=0.05,
        samples=100,
        smoothing=0.9,
    ):
        self.ads = ads
        self.vrx_channel = vrx_channel
        self.vry_channel = vry_channel

        self.deadzone = deadzone
        self.samples = samples
        self.smoothing = smoothing

        self.x_filtered = 0.0
        self.y_filtered = 0.0

    def read_value(self):
        raw_x, raw_y = self.read_raw()

        x = normalize(raw_x)
        y = normalize(raw_y)

        self.x_filtered = self._apply_smoothing(x, self.x_filtered)
        self.y_filtered = self._apply_smoothing(y, self.y_filtered)

        return self.x_filtered, self.y_filtered

    def read_raw(self):
        return (
            self.ads.read(channel1=self.vrx_channel),
            self.ads.read(channel1=self.vry_channel),
        )

    def _sample(self, samples=None, delay=0.002):
        samples = samples or self.samples

        x_values = []
        y_values = []

        for _ in range(samples):
            x, y = self.read_raw()

            x_values.append(x)
            y_values.append(y)

            time.sleep(delay)

        return x_values, y_values

    def _apply_smoothing(self, current, previous):
        alpha = self.smoothing
        return previous + alpha * (current - previous)
