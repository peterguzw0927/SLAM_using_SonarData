# Software Documentation

This document provides an overview of the software modules, dependencies, and instructions for installation.

## Overview of Main Software Modules

### process_xtf_files.py
- Read and sort sonar structs by timestamp
- Return the X(longitude) and Y(latitude) coordinates of the vehicle

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

###https://nav_data.py/

### plotting.py
  -
  
## Flow Chart

![Flow Chart](https://github.com/peterguzw0927/Senior_Design/assets/130591044/55051beb-e09a-4852-8ec7-d313dbbab899)

## Installation Guide

To install the project software stack from scratch, follow these steps:

### 1. Prerequisites

#### holoocean==0.5.8
- Holoocean is a simulator operated on Unreal Engine4, which can be used to generate sonar datasets (IMU though).

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

In the terminal:

```bash
git clone https://github.com/peterguzw0927/Senior_Design.git
cd ../path/to/Senior_Design
pip install -r requirements.txt
