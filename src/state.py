class State:
    def __init__(self, roll, pitch, yaw) -> None:
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def update(self, roll, pitch, yaw):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
