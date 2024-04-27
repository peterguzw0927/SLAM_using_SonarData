# Software Documentation

This document provides an overview of the software modules, dependencies, and instructions for installation.

## Overview of Main Software Modules

### cSlam.py
- Main function for sonarSlam implementation

### process_xtf_files.py
- Read and sort sonar structs by timestamp
- Return the X(longitude) and Y(latitude) coordinates of the vehicle
- `get_xy_coordinates(packet)`:This function extracts the xy-coordinates from a packet, intended for coordinate-based sorting. However, it is currently unused in the code.
- `get_timestamp(packet): `This function extracts the timestamp components (year, month, day, hour, minute, second, hundredths of a second) from a packet, facilitating timestamp-based sorting.
- `xtf_read_sort(directory):`This function reads XTF files from a specified directory. For each file, it reads the packets, extracts sonar packets, and organizes them into a list. It then sorts this list based on timestamps extracted from the packets using the get_timestamp() function, returning the sorted list of sonar data structures.

### landmark_detection.py
- Transform sonar pings from 16-bit to 8-bit for image processing with CV2
- Detects dark and bright contours in the side-scan sonar image
- Merge contours and filter them based on area thresholds
- Computes the center of each contour and adjusts contour coordinates with respect to the center of the image
- Convert pixel coordinates to geographical coordinates using a predefined frame instance
- Retrieves all landmark coordinates from segmented paths

### pixeltogeo.py
- Defines a Python class called frame that represents a coordinate system for sonar side-scan data
- Computes rotation and scale factors based on the frame's parameters
- Convert pixel coordinates to geographic coordinates

### nav_data.py
- Obtain robot coordinates from navigation data
- Segment paths to isolate straight passes of the robot
- Group landmarks within a certain threshold distance

### make_graph.py
- Process the sonar data to identify potential landmarks and associate them with known landmarks
- Create a graph structure representing the robot's trajectory and landmark positions for optimization
- The function iterates over each element (sonar struct) in the sonar_struct_list.
- For each sonar struct, it extracts the robot's coordinates (x_coord, y_coord), heading (heading), and timestamp using the get_timestamp function.
- It then retrieves sonar data from the struct and processes it to identify potential landmarks using the get_landmarks function.
- Next, it associates these potential landmarks with known landmarks within a certain radius, using the associate_landmarks function.
- Optionally, if plot=True, it generates a plot showing the robot's path, potential landmarks seen by the robot, and confirmed landmarks from the landmark_list.

### plotting.py
- Various plots depicting robot path, detected landmarks, and other relevant information
- `plot_landmarks(robot_coordinates, landmark_coordinates, grouped_coordinates=None, grouping_threshold=-8)`: Plots the robot's path and detected landmarks. Optionally, it can also plot grouped landmarks within a specified range.
- `plot_path(sonar_struct_list)`: Extracts and plots position data from sonar structs, coloring the points based on the robot's heading.
- `plot_over_time(sonar_struct_list)`: Plots robot positions with colors based on timestamps, and writes the data to a CSV file.
- `plot_sorted_sonar_structs(sorted_sonar_structs)`: Plots all sonar structs from a sorted list, with colors based on their position in the list.
- `plot_segmented_paths(linear_sections)`: Plots linear sections of the robot's path, each section in a different color.
- `plot_segments_landmarks(segmented_paths)`: Plots linear segments of the robot's path and landmarks, each segment in a different color.
  
## Flow Chart

![Flow Chart](https://github.com/peterguzw0927/Senior_Design/assets/130591044/55051beb-e09a-4852-8ec7-d313dbbab899)

## Installation Guide

To install the project software stack from scratch, follow these steps:

### 1. Prerequisites

#### matplotlib>=3.8.0
- Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.

#### pandas>=1.1.4
- Pandas is a powerful data manipulation and analysis library, providing data structures and functions to work with structured data.

#### seaborn>=0.11.0
- Seaborn is a statistical data visualization library based on Matplotlib, providing a high-level interface for drawing attractive and informative statistical graphics.

#### pyxtf>=1.4.0
- Pyxtf is a library for working with XTF (eXtended Triton Format) files commonly used in marine surveying and oceanography.

#### geopy==2.4.1
- Geopy is a Python library for geocoding and working with geographical data.

#### tqdm>=4.64.0
- Tqdm is a fast, extensible progress bar for Python and CLI, providing visual feedback on the progress of iterables.

#### numpy>=1.23.5
- NumPy is the fundamental package for scientific computing with Python, providing support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions.

#### opencv-python>=4.1.1
- OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library, that provides various algorithms and tools for image and video processing.

### 2. Installation Steps
- Install Python 3.12:
First, ensure you have Python 3.12 installed on your system. You can download the installer from the official Python website (https://www.python.org/downloads/) and follow the installation instructions specific to your operating system.
- Create a Virtual Environment in terminal:
```bash
python3.12 -m venv myenv
```
- Activate the Virtual Environment(Windows):
```bash
myenv\Scripts\activate
```
- Activate the Virtual Environment(Mac):
```bash
source myenv/bin/activate
```
In the terminal:

```bash
git clone https://github.com/peterguzw0927/Senior_Design.git
cd ../path/to/Senior_Design
pip install -r requirements.txt
```
Example (no plotting):

```bash
python cSlam.py '/path/to/xtfDirectory'
```

Example (with plotting):

```bash
python cSlam.py '/path/to/xtfDirectory' True
```

#### 2.1 Installing dataset
- If you haven't download the xtf files from home page:
- Bassurelle Sandbanks SCI: https://drive.google.com/drive/folders/1rM4ISj9gcmGjYNPcOs2p_3LflSpfRMO_?usp=drive_link
- Official Website: https://data.europa.eu/data/datasets/raw-side-scan-sonar-data-from-bassurelle-sandbanks-sci?locale=en

### 3. Installing supplemental materials
#### 3.1 initial_2D_slam
Dependencies:
```bash
pip install numpy
pip install matplotlib
```
Run demo.py or test.py
#### 3.2 Bruce_slam_implementation
Download the vm containing Bruce_SLAM algorithm here:
- https://drive.google.com/file/d/1jbgV3TAxXKJbmPuHgUchFqWUUs6io93y/view?usp=drive_link

After opening the .vm file with vmware workstation 17 pro, password is 123

Adjust the system RAM to at least 16GB

Open up a new terminal
```bash
cd ws_sonar/ 
catkin build
bash s1_run.bash
```
Open up a new terminal
```bash
cd ws_sonar/ 
bash s2_run.bash
```
#### 3.3 HoloOcean
Please refer to this website:
- https://holoocean.readthedocs.io/en/master/usage/installation.html
