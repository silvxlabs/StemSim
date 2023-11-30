import numpy as np


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


def generate_quadrafolium(a):
    theta = np.linspace(0, 2 * np.pi, 100)
    r = a * np.cos(2 * theta)

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    x += 50
    y += 50

    return np.array(x, y)
