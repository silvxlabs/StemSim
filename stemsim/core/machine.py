import numpy as np
from .stem_map import StemMap
from .devices import Camera, GNSS
from .utils import create_2d_transformation_matrix


class Machine:
    """
    A machine that can move around and take pictures of trees.

    Parameters
    ----------
    stem_map: StemMap
        The stem map to place the machine in.
    camera : Camera
        The camera device.
    gnss : GNSS
        The GNSS device.

    Attributes
    ----------
    stem_map: StemMap
        The stem map.
    camera : Camera
        The camera device.
    gnss : GNSS
        The GNSS device.
    pose : tuple[float, float, float]
        The current pose of the machine.

    Methods
    -------
    move(distance, rotation)
        Move the machine.
    get_stems(stem_map)
        Get the stems from the camera.
    """

    def __init__(self, stem_map: StemMap, camera: Camera, gnss: GNSS):
        """Constructor"""
        self.stem_map = stem_map
        self.camera = camera
        self.gnss = gnss

    @property
    def pose(self) -> tuple[float, float, float]:
        """
        The current pose of the machine.

        Returns
        -------
        tuple[float, float, float]
            The current pose of the machine.
        """
        return (self.gnss.x, self.gnss.y, self.camera.theta)

    @pose.setter
    def pose(self, pose: tuple[float, float, float]) -> None:
        """
        Set the current pose of the machine.

        Parameters
        ----------
        pose : tuple[float, float, float]
            The current pose of the machine.
        """
        self.gnss.x = pose[0]
        self.gnss.y = pose[1]
        self.camera.theta = pose[2]

    def move(self, distance: float, rotation: float) -> None:
        """
        Move the machine.

        Parameters
        ----------
        distance : float
            Distance to move in meters.
        rotation : float
            Rotation to turn in radians.
        """

        # The pose is derived from the GNSS and camera. So, we need to update
        # both of those devices.
        self.camera.theta += rotation
        self.camera.theta = self.camera.theta % (2 * np.pi)
        self.gnss.x += distance * np.cos(self.camera.theta)
        self.gnss.y += distance * np.sin(self.camera.theta)

    def get_local_stems(self) -> StemMap:
        """
        Get the stems from the camera.

        Returns
        -------
        StemMap
            The stems in the camera's field of view.
        """

        # Compute the transformation matrix from the world frame of reference
        T = create_2d_transformation_matrix(self.gnss.x, self.gnss.y, self.camera.theta)

        # Transform the stem map into the camera's frame of reference
        stem_map_T = self.stem_map.affine_transform(np.linalg.inv(T))

        # Query the transformed stem map using the camera's parameters
        stem_map_local = stem_map_T.query(
            self.camera.max_dist, -self.camera.fov / 2, self.camera.fov / 2
        )

        # Transform the stem map back into the world frame of reference
        stem_map_local = stem_map_local.affine_transform(T)

        return stem_map_local
