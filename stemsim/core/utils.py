import numpy as np


def create_2d_transformation_matrix(x: float, y: float, theta: float) -> np.ndarray:
    """
    Create a 2D transformation matrix.

    Parameters
    ----------
    x : float
        Translation in x direction
    y : float
        Translation in y direction
    theta : float
        Rotation angle in radians.

    Returns
    -------
    T : np.ndarray
        The 3x3 homogenous transformation matrix.
    """

    # Create the rotation part of the matrix
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    R = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])

    # Create the translation vector
    t = np.array([x, y])

    # Combine into a 3x3 homogenous transformation matrix
    T = np.identity(3)
    T[:2, :2] = R
    T[:2, 2] = t

    return T
