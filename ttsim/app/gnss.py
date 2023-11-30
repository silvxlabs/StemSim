import numpy as np


class GNSS:
    def __init__(self, position: tuple[float, float] = (0, 0), hdop: float = 1.0):
        self._position = position
        self._hdop = hdop

    @property
    def position(self):
        # Simulate position error based on HDOP
        error_magnitude = self._hdop * 5  # Arbitrary scaling factor
        error = np.random.normal(0, error_magnitude, 2)
        simulated_position = (
            self._position[0] + error[0],
            self._position[1] + error[1],
        )
        return simulated_position

    @position.setter
    def position(self, position: tuple[float, float]):
        self._position = position

    @property
    def hdop(self):
        return self._hdop

    @hdop.setter
    def hdop(self, hdop: float):
        if hdop < 0:
            raise ValueError("HDOP cannot be negative")
        self._hdop = hdop
