"""
This is an example Python client for the API. Assumes the Docker container
is running on localhost:80. A similar client could be written in C# for the
AR component integration. Note: I'm only using endpoint I need for the example.
"""

import requests

BASE_URL = "http://127.0.0.1:80"


# =============================================================================
# Stem map endpoint consumers
# =============================================================================
def create_stem_map(
    width: int, height: int, tph: float, dbh_mu: float, dbh_sigma: float
):
    response = requests.post(
        f"{BASE_URL}/stem-maps",
        json={
            "width": width,
            "height": height,
            "tph": tph,
            "dbh_mu": dbh_mu,
            "dbh_sigma": dbh_sigma,
        },
    )
    return response.json()


def get_stem_map(stem_map_id):
    response = requests.get(f"{BASE_URL}/stem-maps/{stem_map_id}")
    return response.json()


def list_stem_maps():
    response = requests.get(f"{BASE_URL}/stem-maps")
    return response.json()


# =============================================================================
# Machine endpoint consumers
# =============================================================================
def create_machine(stem_map_id, camera_max_dist, camera_fov):
    response = requests.post(
        f"{BASE_URL}/machines",
        json={
            "stem_map_id": stem_map_id,
            "camera_max_dist": camera_max_dist,
            "camera_fov": camera_fov,
        },
    )
    return response.json()


def get_machine(machine_id):
    response = requests.get(f"{BASE_URL}/machines/{machine_id}")
    return response.json()


def list_machines():
    response = requests.get(f"{BASE_URL}/machines")
    return response.json()


def set_pose(machine_id, x, y, theta):
    response = requests.patch(
        f"{BASE_URL}/machines/{machine_id}/pose",
        json={
            "machine_id": machine_id,
            "x": x,
            "y": y,
            "theta": theta,
        },
    )

    return response.json()


def move_machine(machine_id, distance, rotation):
    response = requests.patch(
        f"{BASE_URL}/machines/{machine_id}/move",
        json={
            "machine_id": machine_id,
            "distance": distance,
            "rotation": rotation,
        },
    )

    return response.json()


def get_local_stems(machine_id):
    response = requests.get(f"{BASE_URL}/machines/{machine_id}/local-stems")
    return response.json()
