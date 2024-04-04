import pyxtf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2

def plot_xtf(file_path):
    # Read the XTF file
    (file_header, packets) = pyxtf.xtf_read(file_path)
    # print('The following (supported) packets are present (XTFHeaderType:count): \n\t' +
    #   str([key.name + ':{}'.format(len(v)) for key, v in packets.items()]))
    packet_sizes = {key.name: len(value) for key, value in packets.items()}

    # Get the sonar channel data
    sonar_channel_data = packets[pyxtf.XTFHeaderType.sonar]

    # Initialize arrays to store the data
    longitude = []
    latitude = []
    depth = []
    heading = []

    # Iterate through each ping and extract the data
    for ping in sonar_channel_data:
        # Extract sensor coordinates and heading
        longitude.append(ping.SensorXcoordinate)
        latitude.append(ping.SensorYcoordinate)
        depth.append(ping.SensorDepth)
        heading.append(ping.SensorHeading)

    # Concatenate sonar channel data
    np_chan1 = pyxtf.concatenate_channel(sonar_channel_data, file_header=file_header, channel=0, weighted=True)
    np_chan2 = pyxtf.concatenate_channel(sonar_channel_data, file_header=file_header, channel=1, weighted=True)

    # Clip data to remove outliers
    upper_limit = 2 ** 40
    np_chan1.clip(0, upper_limit-1, out=np_chan1)
    np_chan2.clip(0, upper_limit-1, out=np_chan2)

    # # # Apply logarithmic transformation
    np_chan1 = np.log10(np_chan1 + 0.0001)
    np_chan2 = np.log10(np_chan2 + 0.0001)

    # Transpose arrays if needed
    if np_chan1.shape[0] > np_chan1.shape[1]:
        np_chan1 = np_chan1.T
    if np_chan2.shape[0] > np_chan2.shape[1]:
        np_chan2 = np_chan2.T

    # Plot the waterfall view
    merged_image = np.hstack((np_chan1, np_chan2))
    # plt.figure(figsize=(12, 6))
    # plt.imshow(merged_image, cmap='gray')
    # plt.axis('off')  # Turn off axes
    # plt.show()

    # img = ((merged_image / 65536.0) * 255.0).astype(np.uint8) #Converting to 8 bit
    # #print(img.shape)
    # print(img)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    
    return merged_image, longitude, latitude, depth, heading

