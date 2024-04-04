import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ReadSonar import plot_xtf  # Assuming this function works as expected

# Directory where the files are located
data_directory = r'C:\Users\xingl\Downloads\JNCC2013_03BassSandRawAcousticssraw_data\BoxA'
files = os.listdir(data_directory)

# Filter out files with 0KB size
files = [file for file in files if os.path.getsize(os.path.join(data_directory, file)) > 0]

# Filter and sort remaining files based on timestamp
image_files = [file for file in files if file.endswith('L.xtf')]

# Custom sort function to sort files based on timestamp in the filename
def sort_by_timestamp(filename):
    timestamp = filename[:14]  # Extract timestamp from filename
    return int(timestamp)

# Sort image_files based on timestamp
image_files = sorted(image_files, key=sort_by_timestamp)

# Plotting
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
plt.figure(figsize=(10, 8))

# Process each file
for filename in image_files[:5]:
    print(filename)
    file_path = os.path.join(data_directory, filename)  # Construct full file path
    img, longitude, latitude, depth, heading = plot_xtf(file_path)  # Process the file with the appropriate path
    # Plot vehicle locations
    # ax.scatter(longitude, latitude, depth, c=heading, cmap='viridis')
    # ax.set_xlabel('Longitude')
    # ax.set_ylabel('Latitude')
    # ax.set_zlabel('Depth')
    # plt.title('Vehicle Locations')
    # plt.pause(0.1)  # Pause to update the plot
    plt.imshow(img, cmap='gray', alpha=0.5)


plt.title('Sonar Images')
plt.show()
