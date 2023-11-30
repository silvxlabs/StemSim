import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
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
    ax.set_xlim(0, stem_map.width)
    ax.set_ylim(0, stem_map.height)

    # Set aspect ratio to 1
    ax.set_aspect(1)

    plt.show()
