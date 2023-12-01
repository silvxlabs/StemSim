import requests
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np

BASE_URL = "http://127.0.0.1:8000"


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


def set_pose(x, y, theta):
    response = requests.patch(
        f"{BASE_URL}/machine/pose",
        json={
            "x": x,
            "y": y,
            "theta": theta,
        },
    )
    return response.json()


def move_machine(distance, rotation):
    response = requests.patch(
        f"{BASE_URL}/machine/move",
        json={
            "distance": distance,
            "rotation": rotation,
        },
    )

    return response.json()


def get_stems():
    response = requests.get(f"{BASE_URL}/camera/stems")
    return response.json()


def get_all_stems():
    response = requests.get(f"{BASE_URL}/stemmap")
    return response.json()


def run():
    all_stems = get_all_stems()
    set_pose(50, 0, np.pi / 2)
    for i in range(20):
        move_machine(5, 0)
        stems = get_stems()
        show_stem_map(all_stems, stems)


run()
