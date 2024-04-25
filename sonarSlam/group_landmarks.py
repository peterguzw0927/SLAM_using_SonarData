'''
Contains methods to group nearby landmarks points as one single landmark
'''
import numpy as np
from geopy.distance import geodesic



def group_landmarks(landmark_coordinates, threshold=0.08):
    '''Groups landmarks based on Euclidean distance'''
    grouped_coordinates = []

    for coord1 in landmark_coordinates:
        grouped = False
        for group in grouped_coordinates:
            mean_coord = np.mean(group, axis=0)
            if geodesic(mean_coord, coord1).kilometers < threshold:
                group.append(coord1)
                grouped = True
                break
        if not grouped:
            grouped_coordinates.append([coord1])

    # Convert lists of coordinates to tuples
    grouped_coordinates = [tuple(np.mean(group, axis=0)) for group in grouped_coordinates]
    
    return grouped_coordinates