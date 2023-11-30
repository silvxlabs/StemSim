from pydantic import BaseModel


class Move(BaseModel):
    distance: float
    rotation: float


class Pose(BaseModel):
    x: float
    y: float
    theta: float


class Stem(BaseModel):
    uid: int
    x: float
    y: float
    dbh: float
    cut: bool


class Stems(BaseModel):
    stems: list[Stem]
