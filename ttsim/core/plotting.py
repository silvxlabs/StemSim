import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np
from .stem_map import StemMap


def show_stem_map(stem_map: StemMap):
    # Use Circle patches to represent the stems
    patches = []
    for x, y, dbh in zip(stem_map.x, stem_map.y, stem_map.dbh):
        patches.append(plt.Circle((x, y), dbh / 200))

    # Create a collection of the patches
    collection = PatchCollection(patches, fc="green", ec="black", alpha=0.5)

    # Add the collection to the plot
    _, ax = plt.subplots()
    ax.add_collection(collection)

    # Set the plot limits to the stem map extents
    ax.set_xlim(np.min(stem_map.x), np.max(stem_map.x))
    ax.set_ylim(np.min(stem_map.y), np.max(stem_map.y))

    # Set aspect ratio to 1
    ax.set_aspect(1)

    plt.show()
