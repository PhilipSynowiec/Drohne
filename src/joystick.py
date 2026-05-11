import time

from machine import ADC

MAX_INT = 65535


def normalize(value):
    return 2 * value / MAX_INT - 1.0


class Joystick:
    def __init__(
        self,
        vrx_pin,
        vry_pin,
        deadzone=0.05,
        samples=100,
        smoothing=0.9,
    ):
        """
        `deadzone`: normalized deadzone (0.0 - 1.0)
        `smoothing`: EMA filter coefficient
        `max_angle`: value read when stick is farthest from center
        """

        self.x_adc = ADC(vrx_pin)
        self.y_adc = ADC(vry_pin)

        self.deadzone = deadzone
        self.samples = samples
        self.smoothing = smoothing

        self.x_filtered = 0.0
        self.y_filtered = 0.0

    # -------------------------------------------------
    # Reading Values
    # -------------------------------------------------

    def read_value(self):
        """
        Returns:
            x, y in range -1.0 to 1.0
        """

        raw_x, raw_y = self.read_raw()

        x = normalize(raw_x)
        y = normalize(raw_y)

        # EMA smoothing
        #  WARNING: might be harmful for rapid movements
        self.x_filtered = self._apply_smoothing(
            x,
            self.x_filtered,
        )

        self.y_filtered = self._apply_smoothing(
            y,
            self.y_filtered,
        )

        return (
            self.x_filtered,
            self.y_filtered,
        )

    # -------------------------------------------------
    # Raw ADC Reading
    # -------------------------------------------------

    def read_raw(self):
        return (
            self.x_adc.read_u16(),
            self.y_adc.read_u16(),
        )

    # -------------------------------------------------
    # Sampling Utilities
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Filtering
    # -------------------------------------------------

    def _apply_smoothing(self, current, previous):
        alpha = self.smoothing
        return previous + alpha * (current - previous)
