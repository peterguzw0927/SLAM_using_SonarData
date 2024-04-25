'''
Segment position data into straight pases
'''

import numpy as np
import matplotlib.pyplot as plt


def segment_paths(sonar_struct_list):
    '''Separates linear sections of the robot's path
    Returns a list containing lists of sonar packets from the same linear section
    '''
    linear_segments = []

    current_headings = [None] * 50  # Check last 50 points to detect turns
    current_sublist = [sonar_struct_list[0]]

    for sonar_struct in sonar_struct_list:
        prev_headings = current_headings[:]
        current_headings.pop(0)
        current_headings.append(sonar_struct.SensorHeading)

        if all(head is not None for head in prev_headings) and \
           any(abs(sonar_struct.SensorHeading - prev_headings[i]) > 80 for i in range(50)):
            linear_segments.append(current_sublist)
            current_sublist = [sonar_struct]
        else:
            current_sublist.append(sonar_struct)

    linear_segments.append(current_sublist)

    # Filter out segments with length less than 1000
    filtered_segments = [segment for segment in linear_segments if len(segment) >= 1000]

    return filtered_segments

def get_position_data(sonar_struct_list):
    '''Returns list of robot's coordinates extracted from sonar structs
    '''
    robot_coordinates = []
    for sonar_struct in sonar_struct_list:
        robot_coordinates.append((sonar_struct.SensorYcoordinate, sonar_struct.SensorXcoordinate))

    return robot_coordinates






