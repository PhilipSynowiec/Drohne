from machine import ADC
import time


class Joystick:
    def __init__(
        self,
        pins=(26, 27),
        max_value_x=30,
        max_value_y=30,
        deadzone=0.05,
        samples=100,
        smoothing=0.2,
    ):
        """
        `deadzone`: normalized deadzone (0.0 - 1.0)
        `smoothing`: EMA filter coefficient
        `max_angle`: value read when stick is farthest from center
        """

        self.x_adc = ADC(pins[0])
        self.y_adc = ADC(pins[1])

        self.max_value_x = max_value_x
        self.max_value_y = max_value_y
        self.deadzone = deadzone
        self.samples = samples
        self.smoothing = smoothing

        self.x_filtered = 0.0
        self.y_filtered = 0.0

        self.calibrate()

    # -------------------------------------------------
    # Reading Values
    # -------------------------------------------------

    def read_value(self):
        """
        Returns:
            x, y in range -1.0 to 1.0
        """

        raw_x, raw_y = self.read_raw()

        x = self._normalize_axis(
            raw_x,
            self.center_x,
            self.min_x,
            self.max_x,
        )

        y = self._normalize_axis(
            raw_y,
            self.center_y,
            self.min_y,
            self.max_y,
        )

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

    def read_angle(self):
        """
        Returns:
            x, y as an angle within [-self.max_angle;self.max_angle]
        """

        x, y = self.read_value()

        return (
            int(x * self.max_value_x),
            int(y * self.max_value_y),
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
    # Calibration
    # -------------------------------------------------

    def calibrate(self):
        print("=== Joystick Calibration ===")

        self.center_x, self.center_y = self._calibrate_center()

        self.min_x, self.min_y = self._calibrate_corner(
            "Move joystick LEFT and then DOWN"
        )

        self.max_x, self.max_y = self._calibrate_corner(
            "Move joystick RIGHT and then UP"
        )

        print("Calibration complete.\n")

    def _calibrate_center(self):
        print("Leave joystick centered...")
        time.sleep(1)

        x_vals, y_vals = self._sample(50)

        return (
            sum(x_vals) / len(x_vals),
            sum(y_vals) / len(y_vals),
        )

    def _calibrate_corner(self, message):
        print(message)
        time.sleep(1)

        x_vals, y_vals = self._sample(100)

        return (
            min(x_vals) if "LEFT" in message else max(x_vals),
            min(y_vals) if "DOWN" in message else max(y_vals),
        )

    # -------------------------------------------------
    # Normalization
    # -------------------------------------------------

    def _normalize_axis(self, value, center, minimum, maximum):
        """
        Convert ADC reading to normalized float (-1.0 to 1.0)
        """

        if value >= center:
            span = maximum - center
            normalized = (value - center) / span
        else:
            span = center - minimum
            normalized = (value - center) / span

        # Clamp
        normalized = max(-1.0, min(1.0, normalized))

        # Deadzone
        if abs(normalized) < self.deadzone:
            normalized = 0.0

        return normalized

    # -------------------------------------------------
    # Filtering
    # -------------------------------------------------

    def _apply_smoothing(self, current, previous):
        alpha = self.smoothing
        return previous + alpha * (current - previous)
