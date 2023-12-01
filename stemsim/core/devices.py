from dataclasses import dataclass


@dataclass
class Camera:
    """
    The camera device.

    Parameters
    ----------
    theta : float
        The current angle of the camera in radians.
    max_dist : float
        The maximum distance the camera can see in meters.
    fov : float
        The field of view of the camera in radians.
    """

    theta: float
    max_dist: float
    fov: float


@dataclass
class GNSS:
    """
    The GNSS device.

    Parameters
    ----------
    x : float
        The current x position of the machine in meters.
    y : float
        The current y position of the machine in meters.
    """

    x: float
    y: float
