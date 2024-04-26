# An user implementation of Bruce-slam, friendly to use, no dependency needed.
<img width="625" alt="Screenshot 2024-04-25 at 22 25 51" src="https://github.com/peterguzw0927/Senior_Design/assets/114111503/a867f63c-7140-4087-8a5a-51bdeafd036c">

- A video of our working implementation: https://drive.google.com/file/d/1W8NGoUxOD8sDb5Ks5Um5IE0GSRQNU36G/view?usp=drive_link
## Download steps
Download the vm containing our SLAM algorithm here:
https://drive.google.com/file/d/1jbgV3TAxXKJbmPuHgUchFqWUUs6io93y/view?usp=drive_link

After opening the .vm file with vmware workstation 17 pro, password is 123

Adjust the system RAM to at least 16GB

## How to use ##
Open up a new terminal
- cd ws_sonar/ 
- catkin build
- bash s1_run.bash

Open up a new terminal
- cd ws_sonar/ 
- bash s2_run.bash

## Sample rosbag data ##
- https://drive.google.com/file/d/1nmiFfyk8mVssLqgac7BOe4_RPBP6Wnc9/view
- Reference: https://arxiv.org/abs/2202.08359
- The ros_bag contains DVL data, Depth data,IMU data, and sonar oculus data
- If you want to switch to your own data,make sure you have the right type of senser data
- The sample data comes from a marina at the United States Merchant Marine Academy (USMMA).

## Python Dependency if you want to install from scratch #
```
cv_bridge
gtsam
matplotlib
message_filters
numpy
opencv_python
rosbag
rospy
scikit_learn
scipy
sensor_msgs
Shapely
```
## ROS dependencies 
```
ROS-noetic
catkin-pybind11
catkin-tools
```

- Reference github:https://github.com/jake3991/sonar-SLAM/tree/main/bruce_slam

