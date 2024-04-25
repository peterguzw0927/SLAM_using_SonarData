'''
Basic graph SLAM implementation, largely adopted from tutorial at
https://github.com/DanielsKraus/SLAM-python
'''


import numpy as np
# import data viz resources
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns


def initialize_constraints(N, num_landmarks, initial_pose):
    ''' This function takes in a number of time steps N, number of landmarks, and a start position,
        and returns initialized constraint matrices, omega and xi.'''
    
    ## Recommended: Define and store the size (rows/cols) of the constraint matrix in a variable
    size = (N + num_landmarks)*2
    rows = size
    cols = size

    # Define the constraint matrix, Omega, with two initial "strength" values for the initial x, y location of our robot
    omega = np.zeros((rows,cols))
    
    strength = 1    # 100% confidence in initial position
    
    initial_x = initial_pose[0]
    initial_y = initial_pose[1]
    
    omega[0,0] = strength
    omega[1,1] = strength

    # Define the constraint vector, xi
    xi = np.zeros((rows, 1))
    xi[0] = initial_x
    xi[1] = initial_y

    return omega, xi



# def create_slam_data(sonar_struct_list, landmark_coordinates):
#     ''' Given sonar structs and landmark coordinates, create the data list that gets passed to the slam function

#     Each element of the list looks like:
#         [[[0, -12.35130507136378, 2.585119104239249], [1, -2.563534536165313, 38.22159657838369], [3, -26.961236804740935, -0.4802312626141525]], [-11.167066095509824, 16.592065417497455]], 
#         1st element: list of relevant landmarks for data point with distance data
#         2nd element: dx/dy motion data
#         3rd element: dx motion data (probably irrelevant)
#     '''
#     for sonar_struct in sonar_struct_list




def get_poses_landmarks(mu, N):
    # create a list of poses
    poses = []
    for i in range(N):
        poses.append((mu[2*i].item(), mu[2*i+1].item()))

    # create a list of landmarks
    landmarks = []
    for i in range(num_landmarks):
        landmarks.append((mu[2*(N+i)].item(), mu[2*(N+i)+1].item()))

    # return completed lists
    return poses, landmarks



def slam(data, N, num_landmarks, initial_pose, motion_noise, measurement_noise):
    '''
    data: Each element is list containing measurements, motion, and dx
        -Measurements -> not sure, but likely the distance from given point to a landmark?
        -Motion -> dx and dy
        -dx -> first bin of motion, meaning that motion is probably velocity/acceleration
    '''
    
    ## TODO: Use your initilization to create constraint matrices, omega and xi
    omega, xi = initialize_constraints(N, num_landmarks, initial_pose)
    
    ## TODO: Iterate through each time step in the data
    ## get all the motion and measurement data as you iterate
    for i in range(len(data)):
        measurements = data[i][0]
        motion = data[i][1]
        dx = motion[0]
    
        ## TODO: update the constraint matrix/vector to account for all *measurements*
        ## this should be a series of additions that take into account the measurement noise
        nweight = 1 / measurement_noise
        for m in measurements:
            
            landmark = m[0]
            x = m[1]
            y=  m[2]
            
            omega[2*i, 2*i] += nweight
            omega[2*i, 2*N + 2*landmark] += -nweight
            omega[2*N + 2*landmark, 2*i] += -nweight
            omega[2*N + 2*landmark, 2*N + 2*landmark] += nweight 

            xi[2*i, 0] += -x *nweight
            xi[2*N + 2*landmark, 0] += x *nweight
            
            omega[2*i + 1, 2*i + 1] += nweight
            omega[2*i + 1, 2*N + 2*landmark + 1] += -nweight
            omega[2*N + 2*landmark + 1, 2*i + 1] += -nweight
            omega[2*N + 2*landmark + 1, 2*N + 2*landmark + 1] += nweight
            xi[2*i + 1, 0] += -y *nweight
            xi[2*N + 2*landmark + 1, 0] += y *nweight  
            
     ## TODO: update the constraint matrix/vector to account for all *motion* and motion noise       
        dx = motion[0]             
        dy = motion[1]
        mweight = 1 / motion_noise
    
        omega[2*i, 2*i] +=  mweight
        omega[2*i, 2*i + 2] += - mweight
        omega[2*i + 2, 2*i] += - mweight
        omega[2*i + 2, 2*i + 2] += mweight
        
        xi[2*i, 0] += -dx  * mweight             
        xi[2*i + 2, 0] += dx * mweight   
        
  
        omega[2*i + 1, 2*i + 1] += mweight
        omega[2*i + 1, 2*i + 3] += - mweight
        omega[2*i + 3, 2*i + 1] += - mweight
        omega[2*i + 3, 2*i + 3] += mweight 
        
        xi[2*i + 1, 0] += -dy * mweight
        xi[2*i + 3, 0] += dy * mweight
        
    ## Compute the best estimate of poses and landmark positions
    ## using the formula, omega_inverse * Xi
    mu = np.linalg.inv(np.matrix(omega)) * xi
    return mu # return `mu`

