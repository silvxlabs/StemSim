from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4

from ..core.machine import Machine
from ..core.devices import Camera, GNSS
from .stem_map_router import GetStemMap, stem_map_to_json
from ..db import MACHINES, STEM_MAPS


# =============================================================================
# Data Transfer Objects
# =============================================================================
class ListMachines(BaseModel):
    machines: list[str]


class GetMachine(BaseModel):
    machine_id: str
    camera_max_dist: float
    camera_fov: float
    camera_theta: float
    gnss_x: float
    gnss_y: float


class CreateMachine(BaseModel):
    stem_map_id: str
    camera_max_dist: float
    camera_fov: float


class SetPose(BaseModel):
    x: float
    y: float
    theta: float


class MoveMachine(BaseModel):
    distance: float
    rotation: float


# =============================================================================
# API Endpoints
# =============================================================================

router = APIRouter()


@router.get("/{machine_id}")
async def get_machine(machine_id: str):
    machine = MACHINES[machine_id]
    return GetMachine(
        machine_id=machine_id,
        camera_max_dist=machine.camera.max_dist,
        camera_fov=machine.camera.fov,
        camera_theta=machine.camera.theta,
        gnss_x=machine.gnss.x,
        gnss_y=machine.gnss.y,
    )


@router.get("")
async def list_machines() -> ListMachines:
    return ListMachines(machines=list(MACHINES.keys()))


@router.post("")
async def create_machine(new_machine: CreateMachine) -> GetMachine:
    machine_id = uuid4().hex
    camera = Camera(0, new_machine.camera_max_dist, new_machine.camera_fov)
    gnss = GNSS(0, 0)
    stem_map = STEM_MAPS[new_machine.stem_map_id]
    machine = Machine(stem_map, camera, gnss)
    MACHINES[machine_id] = machine
    return GetMachine(
        machine_id=machine_id,
        camera_max_dist=new_machine.camera_max_dist,
        camera_fov=new_machine.camera_fov,
        camera_theta=0,
        gnss_x=0,
        gnss_y=0,
    )


@router.patch("/{machine_id}/pose")
async def set_pose(machine_id: str, new_pose: SetPose) -> GetMachine:
    machine = MACHINES[machine_id]
    machine.pose = (new_pose.x, new_pose.y, new_pose.theta)
    return GetMachine(
        machine_id=machine_id,
        camera_max_dist=machine.camera.max_dist,
        camera_fov=machine.camera.fov,
        camera_theta=machine.camera.theta,
        gnss_x=machine.gnss.x,
        gnss_y=machine.gnss.y,
    )


@router.patch("/{machine_id}/move")
async def move_machine(machine_id: str, move: MoveMachine) -> GetMachine:
    machine = MACHINES[machine_id]
    machine.move(move.distance, move.rotation)
    return GetMachine(
        machine_id=machine_id,
        camera_max_dist=machine.camera.max_dist,
        camera_fov=machine.camera.fov,
        camera_theta=machine.camera.theta,
        gnss_x=machine.gnss.x,
        gnss_y=machine.gnss.y,
    )


@router.get("/{machine_id}/local-stems")
async def get_stems_from_camera(machine_id: str) -> GetStemMap:
    machine = MACHINES[machine_id]
    local_stems = stem_map_to_json(machine.get_local_stems())
    return GetStemMap(stem_map_id=None, stems=local_stems)
