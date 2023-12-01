import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np

import client


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


if __name__ == "__main__":
    # Create a stem map
    stem_map = client.create_stem_map(100, 100, 1000, 25, 1)

    # Create a machine and initialize its pose to (50, 0, pi/2)
    machine = client.create_machine(stem_map["stem_map_id"], 20, np.deg2rad(110))
    machine = client.set_pose(machine["machine_id"], 50, 0, np.pi / 2)

    # Move the machine 5 meters forward and 0 radians in each iteration
    for i in range(20):
        client.move_machine(machine["machine_id"], 5, 0)
        stems = client.get_local_stems(machine["machine_id"])
        show_stem_map(stem_map, stems)
