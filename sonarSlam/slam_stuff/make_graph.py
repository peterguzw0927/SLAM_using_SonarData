'''
Creates a graph that can be optimized using the g2o package
'''
import g2o
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from tqdm import tqdm
import sys
sys.path.append('../')
from pixeltogeo import frame

def get_timestamp(packet):
    ''' Returns timestamps for timestamp-based sorting
    '''
    return packet.Year, packet.Month, packet.Day, packet.Hour, packet.Minute, packet.Second, packet.HSeconds



def get_landmarks(s_ping, x_coord, y_coord, heading, high_threshold=32000, low_threshold=1000, pixelIToM=0.1, pixelJToM=0.1):
    '''Looks at sonar data in sonar_ping, and gets the coordinates of any points that are
    above high_threshhold or below low_threshhold

    s_ping: tuple containing port and starbord banks of side scan sonar
    x_coord: x coordinate of robot, as read from xtf file
    y_coord: y coordinate of robot, as read from xtf file
    heading: heading of robot
    high_threshhold: Minimum sonar ping value to be considered as a candidate landmark (bright spots)
    low_threshhold: Maximum sonar ping value to be considered as a candidate landmark (dark spots)
    pixelIToM: (m) width of each pixel in meters
    pixelJToM: (m) height of each pixel in meters
    '''

    port_bank = s_ping[0]   # Port side ping
    stbd_bank = s_ping[1]   # Starbord side ping

    port_indices = np.where((port_bank > high_threshold) | (port_bank < low_threshold))[0].astype(int) # Port landmarks indices
    stbd_indices = np.where((stbd_bank > high_threshold) | (stbd_bank < low_threshold))[0].astype(int) # Stbd landmarks indices
    port_indices = port_indices[port_indices<1600] # throw away center artifact
    stbd_indices = stbd_indices[stbd_indices>400]

    frame_instance = frame(x_coord, y_coord, heading, pixelIToM, pixelJToM) # Declare an instance of the frame class

    port_coordinates = frame_instance.pixelToGeo((2000 - port_indices), 0)  # Convert all port indices at once
    port_coordinates = np.concatenate((port_coordinates[1].reshape(-1,1), port_coordinates[0].reshape(-1,1)), axis=1)
    
    stbd_coordinates = frame_instance.pixelToGeo(stbd_indices, 0)
    stbd_coordinates = np.concatenate((stbd_coordinates[1].reshape(-1,1), stbd_coordinates[0].reshape(-1,1)), axis=1)

    local_landmark_coords = np.concatenate((port_coordinates, stbd_coordinates), axis=0)

    return local_landmark_coords



def associate_landmarks(potential_landmark_list, known_landmark_list, threshold=0.01):
    '''Given a list of potential landmarks for a sonar ping, looks for any known landmarks that 
    are within the radius specified by threshold

    potential_landmark_list: contains xy coordinates of potential landmarks for a particular sonar ping
    known_landmark_list: contains xy coordinates of known landmarks found via edge detection
    threshold: (km) radius that counts as a grouping
    '''

    print(potential_landmark_list)
    potential_landmarks = np.array(potential_landmark_list)
    known_landmarks = np.array(known_landmark_list)
    associated_landmarks = []

    for potential_point in potential_landmark_list:
        distances = np.array([geodesic(potential_point, known_point).kilometers for known_point in known_landmark_list])
        print(potential_point)
        within_threshold = known_landmarks[distances < threshold]
        associated_landmarks.extend(within_threshold)

    return associated_landmarks


def create_graph(sonar_struct_list, landmark_list, plot=False):
    '''Creates a graph with robot pose nodes, landmark nodes,
        odometry edges, and measurement edges that can be 
        optimized using the g2o package

    sonar_struct_list: a list of structs containing all relevant information from the robot,
        extracted from an xtf file
    landmark_list: a list of xy coordinates of predetermined landmarks
    '''
    possible_landmarks = []
    coords = []
    associated_landmarks = []

    # Master loop
    for i, s_struct in enumerate(tqdm(sonar_struct_list)):  # Enumerate is for testing
        x_coord = s_struct.SensorXcoordinate
        y_coord = s_struct.SensorYcoordinate
        heading = s_struct.SensorHeading
        timestamp = get_timestamp(s_struct)
        sonar = s_struct.data   # Side scan sonar

        # Add to list for plotting/demonstration purposes
        # if plot:
        coords.extend([np.array((y_coord, x_coord))])
        # possible_landmarks.extend(get_landmarks(sonar, x_coord, y_coord, heading))    # Returns all potential landmarks

        possible_landmarks_local = get_landmarks(sonar, x_coord, y_coord, heading)
        # possible_landmarks.extend(possible_landmarks_local)

        associated_landmarks.extend(associate_landmarks(np.array(possible_landmarks), np.array(landmark_list)))

        # if i == 50:   # Testing
        #   break

    # Convert lists to numpy array
    possible_landmarks = np.array(possible_landmarks)
    associated_landmarks = np.array(associated_landmarks)
    print(associated_landmarks.shape)
    coords = np.array(coords)
    
    if plot:
        plt.figure(figsize=(10, 8)) 
        plt.scatter(coords[:,0], coords[:,1], color='b', label='Robot Path')
        plt.scatter(associated_landmarks[:,0], associated_landmarks[:,1], color='g')
        plt.scatter(possible_landmarks[:,0], possible_landmarks[:,1], color='r', s=1, label='Potential landmarks seen by robot')
        if landmark_list is not None:
            plt.scatter(*zip(*landmark_list), marker='x', label='Confirmed Landmarks')
        plt.legend()
        plt.show()



















