import numpy as np
from .stem_map import StemMap
from .devices import Camera, GNSS
from .utils import create_2d_transformation_matrix


class Machine:
    def __init__(self, camera: Camera, gnss: GNSS):
        self.camera = camera
        self.gnss = gnss

    @property
    def pose(self):
        return (self.gnss.x, self.gnss.y, self.camera.theta)

    def move(self, rotation: float, distance: float):
        # Update the machine pose
        x, y, theta = self.pose
        theta += rotation
        x += distance * np.cos(theta)
        y += distance * np.sin(theta)

        # Update the camera pose
        self.camera.theta = theta

        # Update the GNSS position
        self.gnss.x = x
        self.gnss.y = y

    def get_trees(self, stem_map: StemMap):
        T = create_2d_transformation_matrix(self.gnss.x, self.gnss.y, self.camera.theta)
        stem_map_T = stem_map.affine_transform(np.linalg.inv(T))
        stem_map_local = stem_map_T.query(
            self.camera.max_dist, -self.camera.fov / 2, self.camera.fov / 2
        )

        return stem_map_local._stems
