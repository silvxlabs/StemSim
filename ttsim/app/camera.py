import numpy as np
from .stem_map import StemMap


def create_2d_transformation_matrix(x, y, theta):
    # Create the rotation part of the matrix
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    R = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])

    # Create the translation part
    t = np.array([x, y])

    # Combine into a 3x3 transformation matrix
    T = np.identity(3)
    T[:2, :2] = R
    T[:2, 2] = t

    return T


class Camera:
    def __init__(self, theta, max_dist: float, fov: float):
        self.theta = theta
        self.max_dist = max_dist
        self.fov = fov

    def capture(self, stem_map: StemMap) -> StemMap:
        stem_map_local = stem_map.query(self.max_dist, -self.fov / 2, self.fov / 2)

        return stem_map_local
