from __future__ import annotations
import numpy as np


class StemMap:
    """
    A stem map is a collection of stems with positions and dbh values.

    Parameters
    ----------
    stems : np.ndarray
        An array of stems with the following columns:
        - uid: unique identifier
        - x: x position in meters
        - y: y position in meters
        - dbh: diameter at breast height in centimeters
        - cut: boolean indicating whether the stem is marked to cut

    Attributes
    ----------
    uid : np.ndarray
        Unique identifier for each stem.
    x : np.ndarray
        X position of each stem in meters.
    y : np.ndarray
        Y position of each stem in meters.
    dbh : np.ndarray
        Diameter at breast height of each stem in centimeters.
    cut : np.ndarray
        Boolean indicating whether each stem is marked to cut.

    Methods
    -------
    copy()
        Return a copy of the stem map.
    affine_transform(T)
        Transform the stem map by the given affine transformation matrix.
    query(radius, min_theta, max_theta)
        Query the stem map for stems within the given radius and angle range.
    """

    def __init__(self, stems):
        """Constructor"""
        self._stems = stems

    def copy(self) -> StemMap:
        """
        Return a copy of the stem map.

        Returns
        -------
        StemMap
            A copy of the stem map.
        """
        return StemMap(self._stems.copy())

    @property
    def uid(self) -> np.ndarray:
        """
        Unique identifier for each stem.

        Returns
        -------
        np.ndarray
            The unique identifier for each stem.
        """
        return self._stems[:, 0]

    @property
    def x(self) -> np.ndarray:
        """
        X position of each stem in meters.

        Returns
        -------
        np.ndarray
            The x position of each stem in meters.
        """
        return self._stems[:, 1]

    @x.setter
    def x(self, array: np.ndarray) -> None:
        """
        Set the x position of each stem in meters.

        Parameters
        ----------
        array : np.ndarray
            The x position of each stem in meters.
        """
        self._stems[:, 1] = array

    @property
    def y(self) -> np.ndarray:
        """
        Y position of each stem in meters.

        Returns
        -------
        np.ndarray
            The y position of each stem in meters.
        """
        return self._stems[:, 2]

    @y.setter
    def y(self, array: np.ndarray) -> None:
        """
        Set the y position of each stem in meters.

        Parameters
        ----------
        array : np.ndarray
            The y position of each stem in meters.
        """
        self._stems[:, 2] = array

    @property
    def dbh(self) -> np.ndarray:
        """
        Diameter at breast height of each stem in centimeters.

        Returns
        -------
        np.ndarray
            The diameter at breast height of each stem in centimeters.
        """
        return self._stems[:, 3]

    @property
    def cut(self) -> np.ndarray:
        """
        Boolean indicating whether each stem is marked to cut.

        Returns
        -------
        np.ndarray
            The boolean indicating whether each stem is marked to cut.
        """
        return self._stems[:, 4]

    def affine_transform(self, T: np.ndarray) -> StemMap:
        """
        Transform the stem map by the given affine transformation matrix.

        Parameters
        ----------
        T : np.ndarray
            The 3x3 homogenous transformation matrix.

        Returns
        -------
        StemMap
            The transformed stem map.
        """

        # Compute the transformed x and y positions
        x, y = T.dot(np.array([self.x, self.y, np.ones(len(self.x))]))[:2]

        # Return a new stem map with the transformed positions
        return StemMap(np.array([self.uid, x, y, self.dbh, self.cut]).T)

    def query(
        self, radius: float, min_theta: float = None, max_theta: float = None
    ) -> StemMap:
        """
        Query the stem map for stems within the given radius and angle range.

        Parameters
        ----------
        radius : float
            The radius in meters.
        min_theta : float, optional
            The minimum angle in radians.
        max_theta : float, optional
            The maximum angle in radians.

        Returns
        -------
        StemMap
            A new stem map containing the queried stems.
        """

        # Compute the polar coordinates of each stem
        rho = np.sqrt(self.x**2 + self.y**2)
        theta = np.arctan2(self.y, self.x)

        # If min_theta > max_theta, then the angle range wraps around 2*pi
        if min_theta > max_theta:
            mask = (rho < radius) & ((min_theta < theta) | (theta < max_theta))
        # Otherwise, the angle range is a single interval
        else:
            mask = (rho < radius) & (min_theta < theta) & (theta < max_theta)

        # Return a new stem map with the queried stems
        return StemMap(
            self._stems[mask],
        )

    def to_json(self) -> dict:
        """
        Return a JSON representation of the stem map.

        Returns
        -------
        dict
            A JSON representation of the stem map.
        """
        return {
            "stems": [
                {
                    "uid": int(stem[0]),
                    "x": float(stem[1]),
                    "y": float(stem[2]),
                    "dbh": float(stem[3]),
                    "cut": bool(stem[4]),
                }
                for stem in self._stems
            ]
        }

    def __repr__(self):
        return f"<StemMap {len(self._stems)} stems>"


def generate_stem_map(
    width: int, height: int, tph: float, dbh_mu: float, dbh_sigma: float
) -> StemMap:
    """
    Generate a random stem map.

    Parameters
    ----------
    width : int
        Width of the stem map in meters.
    height : int
        Height of the stem map in meters.
    tph : float
        Trees per hectare.
    dbh_mu : float
        Gaussian mean of the dbh distribution.
    dbh_sigma : float
        Gaussian standard deviation of the dbh distribution.

    Returns
    -------
    StemMap
        A stem map with random stem positions and dbh values.
    """

    # Compute the number of stems to generate based on the trees per hectare and
    # the area of the stem map
    n_stems = int(width * height * tph / 10000)

    # Generate random stem positions and dbh values
    uid = np.arange(n_stems)
    x = np.random.uniform(0, width, n_stems)
    y = np.random.uniform(0, height, n_stems)
    dbh = np.random.normal(dbh_mu, dbh_sigma, n_stems)
    cut = np.zeros(n_stems, dtype=bool)
    # Randomly set 50% of the stems to be marked to cut
    cut[np.random.choice(n_stems, int(n_stems / 2), replace=False)] = True

    # Concatenate the arrays into a single array and transpose
    return StemMap(np.array([uid, x, y, dbh, cut]).T)
