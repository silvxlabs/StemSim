import numpy as np


class StemMap:
    def __init__(self, stems):
        self._stems = stems

    def copy(self):
        return StemMap(self._stems.copy())

    @property
    def uid(self):
        return self._stems[:, 0]

    @property
    def x(self):
        return self._stems[:, 1]

    @x.setter
    def x(self, array: np.ndarray):
        self._stems[:, 1] = array

    @property
    def y(self):
        return self._stems[:, 2]

    @y.setter
    def y(self, array: np.ndarray):
        self._stems[:, 2] = array

    @property
    def dbh(self):
        return self._stems[:, 3]

    @property
    def cut(self):
        return self._stems[:, 4]

    def affine_transform(self, T: np.ndarray):
        x, y = T.dot(np.array([self.x, self.y, np.ones(len(self.x))]))[:2]

        return StemMap(np.array([self.uid, x, y, self.dbh, self.cut]).T)

    def query(self, radius, min_theta=np.pi, max_theta=np.pi / 4):
        rho = np.sqrt(self.x**2 + self.y**2)
        theta = np.arctan2(self.y, self.x)
        if min_theta > max_theta:
            mask = (rho < radius) & ((min_theta < theta) | (theta < max_theta))
        else:
            mask = (rho < radius) & (min_theta < theta) & (theta < max_theta)

        return StemMap(
            self._stems[mask],
        )

    def __repr__(self):
        return f"<StemMap {len(self._stems)} stems>"


def generate_stem_map(
    width: int, height: int, tph: float, dbh_mu: float, dbh_sigma: float
) -> StemMap:
    n_stems = int(width * height * tph / 10000)

    uid = np.arange(n_stems)
    x = np.random.uniform(0, width, n_stems)
    y = np.random.uniform(0, height, n_stems)
    dbh = np.random.normal(dbh_mu, dbh_sigma, n_stems)
    cut = np.zeros(n_stems, dtype=bool)

    return StemMap(np.array(list(zip(uid, x, y, dbh, cut))))
