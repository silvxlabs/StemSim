import requests
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np

BASE_URL = "http://127.0.0.1:80"


def show_stem_map(stems, camera_stems):
    # Use Circle patches to represent the stems
    circles = []
    local_circles = []
    for stem in stems["stems"]:
        circles.append(plt.Circle((stem["x"], stem["y"]), stem["dbh"] / 50))

    for stem in camera_stems["stems"]:
        local_circles.append(plt.Circle((stem["x"], stem["y"]), stem["dbh"] / 50))

    # Create a collection of the patches
    collection = PatchCollection(circles, fc="green", ec="none")
    local_collection = PatchCollection(local_circles, fc="red", ec="none")

    # Add the collection to the plot
    _, ax = plt.subplots()
    ax.add_collection(collection)
    ax.add_collection(local_collection)

    # Set the plot limits to the stem map extents
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    # Set aspect ratio to 1
    ax.set_aspect(1)

    plt.show()


def get_stem_map(stem_map_id):
    response = requests.get(f"{BASE_URL}/stem-maps/{stem_map_id}")
    return response.json()


def list_stem_maps():
    response = requests.get(f"{BASE_URL}/stem-maps")
    return response.json()


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


def run():
    stem_map = create_stem_map(100, 100, 1000, 25, 1)
    machine = create_machine(stem_map["stem_map_id"], 20, np.deg2rad(110))
    machine = set_pose(machine["machine_id"], 50, 50, np.deg2rad(90))
    for i in range(10):
        move_machine(machine["machine_id"], 2, 0)
        stems = get_local_stems(machine["machine_id"])
        show_stem_map(stem_map, stems)


run()

if __name__ == "__main__":
    stem_map = create_stem_map(100, 100, 1000, 25, 1)
    machine = create_machine(stem_map["stem_map_id"], 20, np.deg2rad(110))
    machine_moved = move_machine(machine["machine_id"], 5, 0)
    local_stems = get_local_stems(machine["machine_id"])
    print(local_stems)
