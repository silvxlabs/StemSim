from fastapi import FastAPI
import numpy as np
import uvicorn

from .core.stem_map import generate_stem_map
from .core.machine import Machine
from .core.devices import Camera, GNSS
from .schema import Move, Pose, Stems, Stem

app = FastAPI()

# Generate a stem map
stem_map = generate_stem_map(100, 100, 1000, 25, 5)

# Configure the camera
camera = Camera(theta=np.pi / 2, max_dist=20, fov=np.deg2rad(110))

# Initialize the GNSS receiver
gnss = GNSS(50, 0)

# Initialize the machine
machine = Machine(camera, gnss)


@app.patch("/machine/pose")
async def set_pose(pose: Pose):
    machine.gnss.x = pose.x
    machine.gnss.y = pose.y
    machine.camera.theta = pose.theta
    x, y, theta = machine.pose
    return Pose(x=x, y=y, theta=theta)


@app.patch("/machine/move")
async def move_machine(move: Move):
    machine.move(move.distance, move.rotation)
    x, y, theta = machine.pose
    return Pose(x=x, y=y, theta=theta)


@app.get("/machine/pose")
async def get_machine_pose():
    x, y, theta = machine.pose
    return Pose(x=x, y=y, theta=theta)


@app.get("/camera/stems")
async def get_stems_from_camera():
    stems = machine.get_stems(stem_map)
    return Stems(
        stems=[
            Stem(uid=stem[0], x=stem[1], y=stem[2], dbh=stem[3], cut=stem[4])
            for stem in stems._stems
        ]
    )


@app.get("/stemmap")
async def get_stem_map():
    return Stems(
        stems=[
            Stem(uid=stem[0], x=stem[1], y=stem[2], dbh=stem[3], cut=stem[4])
            for stem in stem_map._stems
        ]
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
