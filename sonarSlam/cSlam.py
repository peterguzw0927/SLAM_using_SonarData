'''
Main function for sonarSlam implementation
'''
import sys
from process_XTF_files import xtf_read_sort
from nav_data import *
from landmark_detection import *
from plotting import *
from group_landmarks import *
from slam_stuff.make_graph import create_graph

import matplotlib.pyplot as plt

def main(directory, plotting=False):
    sonar_struct_list = xtf_read_sort(directory)                # Read xtf files and store sonar pings in a list
    robot_coordinates = get_position_data(sonar_struct_list)    # Get all xy coordinates of robot in a numpy array

    segmented_paths = segment_paths(sonar_struct_list)          # Isolate the straight passes of the robot
    landmark_coordinates = get_landmark_coordinates(segmented_paths, disp_images=plotting) # Get all xy coordinates of landmarks in numpy array

    threshold=0.01  # (km) If two landmarks are within this distance, there are merged into one landmark with location is the mean
    grouped_coordinates = group_landmarks(landmark_coordinates, threshold=threshold)
    
    if plotting:
        plot_landmarks(robot_coordinates, landmark_coordinates, grouped_coordinates, grouping_threshold=threshold)

    # create_graph(sonar_struct_list, landmark_coordinates, plot=plotting)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python main.py <directory containing xtf files> [plotting True/False]")
        sys.exit(1)
    filepath = sys.argv[1]
    plotting = True if len(sys.argv) == 3 and sys.argv[2].lower() == 'true' else False
    main(filepath, plotting)
