import ttsim
import numpy as np

T = ttsim.create_2d_transformation_matrix(50, 50, 0)

stem_map = ttsim.generate_stem_map(100, 100, 1000, 25, 5)
camera = ttsim.Camera(0, 20, np.deg2rad(110))
stem_map_T = stem_map.affine_transform(np.linalg.inv(T))
stem_map_local = camera.capture(stem_map_T)

ttsim.plotting.show_stem_map(stem_map)
ttsim.plotting.show_stem_map(stem_map_local)
