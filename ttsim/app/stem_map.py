import numpy as np


class StemMap:
    def __init__(self, width, height, stems):
        self.width = width
        self.height = height
        self._stems = stems

    @property
    def uid(self):
        return self._stems[:, 0]

    @property
    def x(self):
        return self._stems[:, 1]

    @property
    def y(self):
        return self._stems[:, 2]

    @property
    def dbh(self):
        return self._stems[:, 3]

    @property
    def cut(self):
        return self._stems[:, 4]

    def __repr__(self):
        return f"<StemMap {self._width}x{self._height} {len(self._stems)} stems>"


def generate_stem_map(
    width: int, height: int, tph: float, dbh_mu: float, dbh_sigma: float
) -> StemMap:
    n_stems = int(width * height * tph / 10000)

    uid = np.arange(n_stems)
    x = np.random.uniform(0, width, n_stems)
    y = np.random.uniform(0, height, n_stems)
    dbh = np.random.normal(dbh_mu, dbh_sigma, n_stems)
    cut = np.zeros(n_stems, dtype=bool)

    return StemMap(width, height, np.array(list(zip(uid, x, y, dbh, cut))))
