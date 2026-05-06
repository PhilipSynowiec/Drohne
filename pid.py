def constrain(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def angle_error(target, current):
    error = target - current
    return (error + 180) % 360 - 180


class PID:
    def __init__(self, kp, ki, kd, output_min=-300, output_max=300, integral_limit=100):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.output_min = output_min
        self.output_max = output_max
        self.integral_limit = integral_limit

        self.integral = 0.0
        self.previous_error = 0.0

    def reset(self):
        self.integral = 0.0
        self.previous_error = 0.0

    def update(self, setpoint, measurement, dt):
        error = setpoint - measurement
        return self.update_from_error(error, dt)

    def update_from_error(self, error, dt):
        if dt <= 0:
            return 0.0

        # P
        p = self.kp * error

        # I
        self.integral += error * dt
        self.integral = constrain(
            self.integral,
            -self.integral_limit,
            self.integral_limit
        )
        i = self.ki * self.integral

        # D
        derivative = (error - self.previous_error) / dt
        d = self.kd * derivative

        self.previous_error = error

        output = p + i + d
        output = constrain(output, self.output_min, self.output_max)

        return output