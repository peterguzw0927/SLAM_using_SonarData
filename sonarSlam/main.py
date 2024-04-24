'''
Main file - calls all other modules
'''
from process_XTF_files import xtf_read_sort
from nav_data import *
from landmark_detection import *
from plotting import *
from slam import *
from group_landmarks import *
from slam_g2o import *

import matplotlib.pyplot as plt

directory = "../palau_files"

sonar_struct_list = xtf_read_sort(directory)

# plot_path(sonar_struct_list)
# plot_sorted_sonar_structs(sonar_struct_list)
# plot_over_time(sonar_struct_list)

segmented_paths = segment_paths(sonar_struct_list)
robot_coordinates = np.array(get_position_data(sonar_struct_list))
landmark_coordinates = np.array(get_landmark_coordinates(segmented_paths, disp_images=False))


timesteps = len(robot_coordinates)
num_landmarks = len(landmark_coordinates)	# TODO: Need to cluster landmarks that are close to each other 

# print(landmark_coordinates)

threshold=0.01 # 10 meters - SET TO TYPICAL SIZE OF A BLOB FROM EDGE DETECTION
grouped_coordinates = group_landmarks(landmark_coordinates, threshold=threshold)
plot_landmarks(robot_coordinates, landmark_coordinates, grouped_coordinates, grouping_threshold=threshold)


# SLAM Algorithm
graph_slam = GraphSLAM2D(verbose=True)

# Add fixed pose ID #0
# graph_slam.add_fixed_pose(g2o.SE2())


for i, coord in enumerate(robot_coordinates):
	# graph_slam.add_fixed_pose(coord, i)
	graph_slam.add_fixed_pose(g2o.SE2(coord[0], coord[1], i))	# Takes in x, y, theta

# for landmark in landmark_coordinates:
# 	graph_slam.add_landmark(landmark[0], landmark[1], np.eye(2), pose_id=4)


















