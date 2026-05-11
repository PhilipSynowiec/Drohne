import time


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

        self.x_min = 0
        self.x_center = 13200
        self.x_max = 26400

        self.y_min = 0
        self.y_center = 13200
        self.y_max = 26400

    def read_value(self):
        raw_x, raw_y = self.read_raw()

        x = self._normalize_axis(raw_x, self.x_min, self.x_center, self.x_max)
        y = self._normalize_axis(raw_y, self.y_min, self.y_center, self.y_max)

        x = self._apply_deadzone(x)
        y = self._apply_deadzone(y)

        self.x_filtered = self._apply_smoothing(x, self.x_filtered)
        self.y_filtered = self._apply_smoothing(y, self.y_filtered)

        return self.x_filtered, self.y_filtered

    def read_raw(self):
        return (
            self.ads.read(channel1=self.vrx_channel),
            self.ads.read(channel1=self.vry_channel),
        )

    def calibrate_full(self, duration=10, delay=0.01):
        print("Stick loslassen...")
        time.sleep(1)

        x_values, y_values = self._sample(samples=100)
        self.x_center = sum(x_values) / len(x_values)
        self.y_center = sum(y_values) / len(y_values)

        print("Stick jetzt in alle Richtungen bewegen...")
        start = time.ticks_ms()

        x_min = self.x_center
        x_max = self.x_center
        y_min = self.y_center
        y_max = self.y_center

        while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
            x, y = self.read_raw()

            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x

            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

            time.sleep(delay)

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        print("Kalibrierung fertig:")
        print("x_min:", self.x_min, "x_center:", self.x_center, "x_max:", self.x_max)
        print("y_min:", self.y_min, "y_center:", self.y_center, "y_max:", self.y_max)

    def set_calibration(self, x_min, x_center, x_max, y_min, y_center, y_max):
        self.x_min = x_min
        self.x_center = x_center
        self.x_max = x_max

        self.y_min = y_min
        self.y_center = y_center
        self.y_max = y_max

    def _normalize_axis(self, value, min_value, center_value, max_value):
        if value >= center_value:
            result = (value - center_value) / (max_value - center_value)
        else:
            result = (value - center_value) / (center_value - min_value)

        if result > 1.0:
            return 1.0
        if result < -1.0:
            return -1.0

        return result

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

    def _apply_deadzone(self, value):
        if abs(value) < self.deadzone:
            return 0.0
        return value

    def _apply_smoothing(self, current, previous):
        alpha = self.smoothing
        return previous + alpha * (current - previous)
