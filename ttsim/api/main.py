from fastapi import FastAPI
import numpy as np
import uvicorn

from ..core.stem_map import generate_stem_map
from ..core.machine import Machine
from ..core.devices import Camera, GNSS

api = FastAPI()

stem_map = generate_stem_map(100, 100, 1000, 25, 5)
camera = Camera(0, 20, np.deg2rad(110))
gnss = GNSS(0, 0, 0)
machine = Machine(camera, gnss)


@api.patch("/move")
def move_machine():
    pass


@api.get("/pose")
def get_machine_pose():
    pass


@api.get("/trees")
def get_trees_from_camera():
    pass


if __name__ == "__main__":
    uvicorn.run("main:api", host="127.0.0.1", port=8000, reload=True)
