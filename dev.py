import ttsim.core as sim
import numpy as np

T = sim.utils.create_2d_transformation_matrix(50, 50, 0)

stem_map = sim.generate_stem_map(100, 100, 1000, 25, 5)
camera = sim.Camera(theta=0, max_dist=20, fov=np.deg2rad(110))
gnss = sim.GNSS(x=0, y=0)
machine = sim.Machine(camera, gnss)


print(machine.get_trees(stem_map))

print(machine.pose)
machine.move(np.deg2rad(45), 10)
print(camera.theta)
print(gnss.x, gnss.y)


# sim.plotting.show_stem_map(stem_map)
# sim.plotting.show_stem_map(stem_map_local)
