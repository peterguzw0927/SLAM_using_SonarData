import numpy as np
from helpers import make_data
from helpers import display_world
# import data viz resources
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns

def initialize_constraints(N, num_landmarks, world_size):
    ''' This function takes in a number of time steps N, number of landmarks, and a world_size,
        and returns initialized constraint matrices, omega and xi.'''
    
    ## Recommended: Define and store the size (rows/cols) of the constraint matrix in a variable
    size = (N + num_landmarks)*2
    rows = size
    cols = size

    ## TODO: Define the constraint matrix, Omega, with two initial "strength" values
    ## for the initial x, y location of our robot
    omega = np.zeros((rows,cols))
    
    strength = 1
    
    mid = world_size / 2
    initial_x = mid
    initial_y = mid
    
    omega[0,0] = strength
    omega[1,1] = strength
    ## TODO: Define the constraint *vector*, xi
    ## you can assume that the robot starts out in the middle of the world with 100% confidence
    xi = np.zeros((rows, 1))
    xi[0] = initial_x
    xi[1] = initial_y
    return omega, xi

# a helper function that creates a list of poses and of landmarks for ease of printing
# this only works for the suggested constraint architecture of interlaced x,y poses
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


def print_all(poses, landmarks):
    print('\n')
    print('Estimated Poses:')
    for i in range(len(poses)):
        print('['+', '.join('%.3f'%p for p in poses[i])+']')
    print('\n')
    print('Estimated Landmarks:')
    for i in range(len(landmarks)):
        print('['+', '.join('%.3f'%l for l in landmarks[i])+']')
        
## TODO: Complete the code to implement SLAM

## slam takes in 6 arguments and returns mu, 
## mu is the entire path traversed by a robot (all x,y poses) *and* all landmarks locations
def slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise):
    
    ## TODO: Use your initilization to create constraint matrices, omega and xi
    omega, xi = initialize_constraints(N, num_landmarks, world_size)
    
    ## TODO: Iterate through each time step in the data
    ## get all the motion and measurement data as you iterate
    for i in range(len(data)):
        measurements = data[i][0]
        motion = data[i][1]
        dx = motion[0]

        print("measurements: ", measurements, "motion", motion, "dx", dx)
    
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

# your implementation of slam should work with the following inputs
# feel free to change these input values and see how it responds!

# world parameters
num_landmarks      = 5        # number of landmarks
N                  = 20       # time steps
world_size         = 100.0    # size of world (square)

# robot parameters
measurement_range  = 50.0     # range at which we can sense landmarks
motion_noise       = 2.0      # noise in robot motion
measurement_noise  = 2.0      # noise in the measurements
distance           = 20.0     # distance by which robot (intends to) move each iteratation 


# make_data instantiates a robot, AND generates random landmarks for a given world size and number of landmarks
# data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)

# # call your implementation of slam, passing in the necessary parameters
# mu = slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise)

# # print out the resulting landmarks and poses
# if(mu is not None):
#     # get the lists of poses and landmarks
#     # and print them out
#     poses, landmarks = get_poses_landmarks(mu, N)
#     print_all(poses, landmarks)
    


test_data1 = [[[[1, 19.457599255548065, 23.8387362100849], [2, -13.195807561967236, 11.708840328458608], [3, -30.0954905279171, 15.387879242505843]], [-12.2607279422326, -15.801093326936487]], 
              [[[2, -0.4659930049620491, 28.088559771215664], [4, -17.866382374890936, -16.384904503932]], [-12.2607279422326, -15.801093326936487]], 
              [[[4, -6.202512900833806, -1.823403210274639]], [-12.2607279422326, -15.801093326936487]], 
              [[[4, 7.412136480918645, 15.388585962142429]], [14.008259661173426, 14.274756084260822]], 
              [[[4, -7.526138813444998, -0.4563942429717849]], [14.008259661173426, 14.274756084260822]], 
              [[[2, -6.299793150150058, 29.047830407717623], [4, -21.93551130411791, -13.21956810989039]], [14.008259661173426, 14.274756084260822]], 
              [[[1, 15.796300959032276, 30.65769689694247], [2, -18.64370821983482, 17.380022987031367]], [14.008259661173426, 14.274756084260822]], 
              [[[1, 0.40311325410337906, 14.169429532679855], [2, -35.069349468466235, 2.4945558982439957]], [14.008259661173426, 14.274756084260822]], 
              [[[1, -16.71340983241936, -2.777000269543834]], [-11.006096015782283, 16.699276945166858]], 
              [[[1, -3.611096830835776, -17.954019226763958]], [-19.693482634035977, 3.488085684573048]], 
              [[[1, 18.398273354362416, -22.705102332550947]], [-19.693482634035977, 3.488085684573048]], 
              [[[2, 2.789312482883833, -39.73720193121324]], [12.849049222879723, -15.326510824972983]], 
              [[[1, 21.26897046581808, -10.121029799040915], [2, -11.917698965880655, -23.17711662602097], [3, -31.81167947898398, -16.7985673023331]], [12.849049222879723, -15.326510824972983]], 
              [[[1, 10.48157743234859, 5.692957082575485], [2, -22.31488473554935, -5.389184118551409], [3, -40.81803984305378, -2.4703329790238118]], [12.849049222879723, -15.326510824972983]], 
              [[[0, 10.591050242096598, -39.2051798967113], [1, -3.5675572049297553, 22.849456408289125], [2, -38.39251065320351, 7.288990306029511]], [12.849049222879723, -15.326510824972983]], 
              [[[0, -3.6225556479370766, -25.58006865235512]], [-7.8874682868419965, -18.379005523261092]], 
              [[[0, 1.9784503557879374, -6.5025974151499]], [-7.8874682868419965, -18.379005523261092]], 
              [[[0, 10.050665232782423, 11.026385307998742]], [-17.82919359778298, 9.062000642947142]], 
              [[[0, 26.526838150174818, -0.22563393232425621], [4, -33.70303936886652, 2.880339841013677]], [-17.82919359778298, 9.062000642947142]]]

##  Test Case 1
##
# Actual Pose(s):
Poses1=[[50.000, 50.000],
    [37.858, 33.921],
    [25.905, 18.268],
    [13.524, 2.224],
    [27.912, 16.886],
    [42.250, 30.994],
    [55.992, 44.886],
    [70.749, 59.867],
    [85.371, 75.230],
    [73.831, 92.354],
    [53.406, 96.465],
    [34.370, 100.134],
    [48.346, 83.952],
    [60.494, 68.338],
    [73.648, 53.082],
    [86.733, 38.197],
    [79.983, 20.324],
    [72.515, 2.837],
    [54.993, 13.221],
    [37.164, 22.283]]


#  Actual Landmarks:
Landmark1=[[82.679, 13.435],
    [70.417, 74.203],
    [36.688, 61.431],
    [18.705, 66.136],
    [20.437, 16.983]]


### Uncomment the following three lines for test case 1 and compare the output to the values above ###

mu_1 = slam(test_data1, 20, 5, 100.0, 2.0, 2.0)
poses, landmarks = get_poses_landmarks(mu_1, 20)
print_all(poses, landmarks)

test_data2 = [[[[0, 26.543274387283322, -6.262538160312672], [3, 9.937396825799755, -9.128540360867689]], [18.92765331253674, -6.460955043986683]], 
              [[[0, 7.706544739722961, -3.758467215445748], [1, 17.03954411948937, 31.705489938553438], [3, -11.61731288777497, -6.64964096716416]], [18.92765331253674, -6.460955043986683]], 
              [[[0, -12.35130507136378, 2.585119104239249], [1, -2.563534536165313, 38.22159657838369], [3, -26.961236804740935, -0.4802312626141525]], [-11.167066095509824, 16.592065417497455]], 
              [[[0, 1.4138633151721272, -13.912454837810632], [1, 8.087721200818589, 20.51845934354381], [3, -17.091723454402302, -16.521500551709707], [4, -7.414211721400232, 38.09191602674439]], [-11.167066095509824, 16.592065417497455]], 
              [[[0, 12.886743222179561, -28.703968411636318], [1, 21.660953298391387, 3.4912891084614914], [3, -6.401401414569506, -32.321583037341625], [4, 5.034079343639034, 23.102207946092893]], [-11.167066095509824, 16.592065417497455]], 
              [[[1, 31.126317672358578, -10.036784369535214], [2, -38.70878528420893, 7.4987265861424595], [4, 17.977218575473767, 6.150889254289742]], [-6.595520680493778, -18.88118393939265]], 
              [[[1, 41.82460922922086, 7.847527392202475], [3, 15.711709540417502, -30.34633659912818]], [-6.595520680493778, -18.88118393939265]], 
              [[[0, 40.18454208294434, -6.710999804403755], [3, 23.019508919299156, -10.12110867290604]], [-6.595520680493778, -18.88118393939265]], 
              [[[3, 27.18579315312821, 8.067219022708391]], [-6.595520680493778, -18.88118393939265]],
              [[], [11.492663265706092, 16.36822198838621]], 
              [[[3, 24.57154567653098, 13.461499960708197]], [11.492663265706092, 16.36822198838621]],
              [[[0, 31.61945290413707, 0.4272295085799329], [3, 16.97392299158991, -5.274596836133088]], [11.492663265706092, 16.36822198838621]], 
              [[[0, 22.407381798735177, -18.03500068379259], [1, 29.642444125196995, 17.3794951934614], [3, 4.7969752441371645, -21.07505361639969], [4, 14.726069092569372, 32.75999422300078]], [11.492663265706092, 16.36822198838621]], 
              [[[0, 10.705527984670137, -34.589764174299596], [1, 18.58772336795603, -0.20109708164787765], [3, -4.839806195049413, -39.92208742305105], [4, 4.18824810165454, 14.146847823548889]], [11.492663265706092, 16.36822198838621]], 
              [[[1, 5.878492140223764, -19.955352450942357], [4, -7.059505455306587, -0.9740849280550585]], [19.628527845173146, 3.83678180657467]], [[[1, -11.150789592446378, -22.736641053247872], [4, -28.832815721158255, -3.9462962046291388]], [-19.841703647091965, 2.5113335861604362]], 
              [[[1, 8.64427397916182, -20.286336970889053], [4, -5.036917727942285, -6.311739993868336]], [-5.946642674882207, -19.09548221169787]], [[[0, 7.151866679283043, -39.56103232616369], [1, 16.01535401373368, -3.780995345194027], [4, -3.04801331832137, 13.697362774960865]], [-5.946642674882207, -19.09548221169787]], 
              [[[0, 12.872879480504395, -19.707592098123207], [1, 22.236710716903136, 16.331770792606406], [3, -4.841206109583004, -21.24604435851242], [4, 4.27111163223552, 32.25309748614184]], [-5.946642674882207, -19.09548221169787]]] 


##  Test Case 2
##
#  Actual Pose(s):

Poses2=[[50.000, 50.000],
    [69.035, 45.061],
    [87.655, 38.971],
    [76.084, 55.541],
    [64.283, 71.684],
    [52.396, 87.887],
    [44.674, 68.948],
    [37.532, 49.680],
    [31.392, 30.893],
    [24.796, 12.012],
    [33.641, 26.440],
    [43.858, 43.560],
    [54.735, 60.659],
    [65.884, 77.791],
    [77.413, 94.554],
    [96.740, 98.020],
    [76.149, 99.586],
    [70.211, 80.580],
    [64.130, 61.270],
    [58.183, 42.175]]


# Actual Landmarks:
Landmark2=[[76.777, 42.415],
    [85.109, 76.850],
    [13.687, 95.386],
    [59.488, 39.149],
    [69.283, 93.654]]


### Uncomment the following three lines for test case 2 and compare to the values above ###

# mu_2 = slam(test_data2, 20, 5, 100.0, 2.0, 2.0)
# poses, landmarks = get_poses_landmarks(mu_2, 20)
# print_all(poses, landmarks)

#evaluation of landmark error
landmark_errors = []
for actual, estimated in zip(Landmark1, landmarks):
    error = np.linalg.norm(np.array(actual) - np.array(estimated))
    landmark_errors.append(error)

mean_landmark_error = np.mean(landmark_errors)
print('Mean of landmark_error: ',mean_landmark_error)

#evaluation of pose error
def calculate_pose_error(actual_pose, estimated_pose):
    # Calculate Euclidean distance between actual and estimated poses
    error = np.linalg.norm(np.array(actual_pose) - np.array(estimated_pose))
    return error

pose_errors = []
for actual, estimated in zip(Poses1, poses):
    # Calculate error between actual and estimated poses
    # You might use Euclidean distance or other appropriate metrics
    error = calculate_pose_error(actual, estimated)  # Define your own function for pose error calculation
    pose_errors.append(error)

mean_pose_error = np.mean(pose_errors)
print('Mean of pose error: ',mean_pose_error)


# Display the final world!

# define figure size
plt.rcParams["figure.figsize"] = (20,20)

# check if poses has been created
if 'poses' in locals():
    # print out the last pose
    print('Last pose: ', poses[-1])
    # display the last position of the robot *and* the landmark positions
    display_world(int(world_size), poses[-1], landmarks)
    
    
    