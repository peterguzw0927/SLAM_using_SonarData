import numpy as np
from helpers import make_data
from helpers import display_world
from robot_class import robot
# import data viz resources
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns

world_size         = 10.0    # size of world (square)
measurement_range  = 5.0     # range at which we can sense landmarks
motion_noise       = 0.2      # noise in robot motion
measurement_noise  = 0.2      # noise in the measurements

r = robot(world_size, measurement_range, motion_noise, measurement_noise)
num_landmarks = 3
r.make_landmarks(num_landmarks)

plt.rcParams["figure.figsize"] = (5,5)

print(r)

r.move(1,2)

print(r)
print('Landmark locations [x,y]: ', r.landmarks)
print(r.sense())
display_world(int(world_size), [r.x, r.y],r.landmarks)
