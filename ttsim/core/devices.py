from dataclasses import dataclass


@dataclass
class Camera:
    theta: float
    max_dist: float
    fov: float


@dataclass
class GNSS:
    x: float
    y: float
