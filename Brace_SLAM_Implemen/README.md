# An user implementation of existing slam algorithm, friendly to use, no dependency needed.
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

# Python Dependency if you want to install from scratch #
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

- Reference github:https://github.com/jake3991/sonar-SLAM/tree/main/bruce_slam

