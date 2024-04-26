import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
from sonarSlam.landmark_detection import get_landmark_coordinates
from matplotlib.patches import Circle
from geopy.distance import distance



def plot_landmarks(robot_coordinates, landmark_coordinates, grouped_coordinates=None, grouping_threshold=0.08):
    plt.figure(figsize=(10, 8))  # Adjust the figsize as needed
    plt.scatter(*zip(*robot_coordinates), label='Robot Path')
    plt.scatter(*zip(*landmark_coordinates), marker='x', label='Detected Landmarks')

    circle_label_added=False
    if grouped_coordinates:
        plt.scatter(*zip(*grouped_coordinates), marker='*', label='Grouped Landmarks')
        for coord in grouped_coordinates:
            circle_radius = grouping_threshold  # in kilometers
            radius_degrees = (circle_radius / 111.32)  # Approximation for small distances
            if not circle_label_added:
                circle_label_added=True
                circle = Circle(coord, radius_degrees, color='r', fill=False, label='Grouping Range')
            else:
                circle = Circle(coord, radius_degrees, color='r', fill=False)
            plt.gca().add_patch(circle)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Robot Path and Detected Landmarks')
    plt.legend()
    plt.show()



def plot_path(sonar_struct_list):
    '''Extracts and plots position data from the sonar structs
    Does not return
    '''
    x_all, y_all, z_all, depth_all, heading_all = [], [], [], [], []

    for sonar_struct in sonar_struct_list:
        x_all.append(sonar_struct.SensorXcoordinate)
        y_all.append(sonar_struct.SensorYcoordinate)
        z_all.append(sonar_struct.SensorPrimaryAltitude + sonar_struct.SensorDepth)
        depth_all.append(sonar_struct.SensorDepth)
        heading_all.append(sonar_struct.SensorHeading)

    x_all = np.array(x_all)
    y_all = np.array(y_all)
    z_all = np.array(z_all)
    depth_all = np.array(depth_all)
    heading_all = np.array(heading_all)

    cmap = plt.get_cmap('hsv')
    norm = plt.Normalize(heading_all.min(), heading_all.max())

    plt.scatter(x_all, y_all, c=heading_all, cmap=cmap, norm=norm, marker='o', label='Robot Position')
    plt.colorbar(label='Heading')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Underwater Robot Position')
    plt.legend()
    plt.show()



def plot_over_time(sonar_struct_list):
    '''Plots robot positions with color based on timestamp
    '''
    def get_timestamp(packet):
        ''' Returns timestamps for timestamp-based sorting
        '''
        timestamp = datetime.datetime(packet.Year, packet.Month, packet.Day,
                                      packet.Hour, packet.Minute, packet.Second,
                                      packet.HSeconds * 10000)  # converting hundredths of seconds to microseconds
        return timestamp.timestamp()  # convert datetime object to Unix timestamp

    output_file = "new.csv"
    # Extract x, y coordinates and timestamps
    x_all = [sonar_struct.SensorXcoordinate for sonar_struct in sonar_struct_list]
    y_all = [sonar_struct.SensorYcoordinate for sonar_struct in sonar_struct_list]
    timestamps_all = [get_timestamp(sonar_struct) for sonar_struct in sonar_struct_list]

    # Write data to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X-coordinate', 'Y-coordinate', 'Timestamp'])
        for x, y, timestamp in zip(x_all, y_all, timestamps_all):
            writer.writerow([x, y, timestamp])




def plot_sorted_sonar_structs(sorted_sonar_structs):
    '''Plots all sonar structs from sorted list with colors based on position
    '''
    n = len(sorted_sonar_structs)
    colors = np.arange(n) / n  # Generate a color gradient based on the index

    x_all = [sonar_struct.SensorXcoordinate for sonar_struct in sorted_sonar_structs]
    y_all = [sonar_struct.SensorYcoordinate for sonar_struct in sorted_sonar_structs]

    plt.scatter(x_all, y_all, c=colors, cmap='viridis', marker='o', label='Robot Position')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Robot Position with Color Gradient')
    plt.colorbar(label='Position in List')
    plt.legend()
    plt.show()



def plot_segmented_paths(linear_sections):
    '''Plots linear sections of the robot's path, each section in a different color
    linear_sections: List of lists containing grouped points from linear passes
    '''
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # List of colors to use for plotting

    for i, sublist in enumerate(linear_sections):
        color = colors[i % len(colors)]  # Get color from the list cyclically
        x_all = [sonar_struct.SensorXcoordinate for sonar_struct in sublist]
        y_all = [sonar_struct.SensorYcoordinate for sonar_struct in sublist]
        plt.scatter(x_all, y_all, color=color, marker='o', label=f'Segment {i+1}')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Segmented Robot Paths')
    plt.show()



def plot_segments_landmarks(segmented_paths):
    '''Plots linear segments and landmarks color coded
    '''
    plt.figure(figsize=(10, 8))  # Adjust the figsize as needed
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']
    for i, linear_segment in enumerate(segmented_paths):
        color = colors[i % len(colors)]
        coord_list = get_landmark_coordinates_segment(linear_segment, disp_images=False)

        x_all = [sonar_struct.SensorXcoordinate for sonar_struct in linear_segment]
        y_all = [sonar_struct.SensorYcoordinate for sonar_struct in linear_segment]

        x_values = [point[0] for point in coord_list]
        y_values = [point[1] for point in coord_list]

        plt.scatter(x_all, y_all, color=color, label="Robot Path" if i == 0 else None)
        plt.scatter(x_values, y_values, color=color, marker='x', s=15, label="Landmarks" if i == 0 else None)

    # Show legend with two categories
    plt.legend()

    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Robot Path and Detected Landmarks')
    plt.show()

