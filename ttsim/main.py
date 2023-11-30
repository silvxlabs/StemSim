from fastapi import FastAPI
import numpy as np
import uvicorn

from core.stem_map import generate_stem_map
from core.machine import Machine
from core.devices import Camera, GNSS
from schema import Move, Pose, Stems, Stem

app = FastAPI()

stem_map = generate_stem_map(100, 100, 1000, 25, 5)
camera = Camera(0, 20, np.deg2rad(110))
gnss = GNSS(0, 0)
machine = Machine(camera, gnss)


@app.patch("/move")
async def move_machine(move: Move):
    machine.move(move.distance, move.rotation)
    x, y, theta = machine.pose
    return Pose(x=x, y=y, theta=theta)


@app.get("/pose")
async def get_machine_pose():
    x, y, theta = machine.pose
    return Pose(x=x, y=y, theta=theta)


@app.get("/stems")
async def get_stems_from_camera():
    stems = machine.get_stems(stem_map)
    stems = [
        {"uid": stem[0], "x": stem[1], "y": stem[2], "dbh": stem[3], "cut": stem[4]}
        for stem in stems
    ]
    return Stems(stems=stems)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
