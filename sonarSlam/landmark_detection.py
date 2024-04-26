'''
Pick out landmarks using Canny edge detection algorithm
'''
import cv2
import numpy as np
import pyxtf
import matplotlib.pyplot as plt
from sonarSlam.pixeltogeo import frame

def merge_contours(bright_contours, dark_contours, max_neighbor_distance):
    merged_bright_contours = []
    unmerged_dark_contours = []
    unmerged_bright_contours = []

    for bright_contour in bright_contours:
        merged_bright = bright_contour
        merged = False
        updated_dark_contours = []  # New list to store dark contours without the contour being merged
        for dark_contour in dark_contours:
            merge_flag = False  # Flag to check if the dark contour is merged
            for point in dark_contour[:, 0]:
                pt = (int(point[0]), int(point[1]))  # Convert coordinates to integers
                dist = cv2.pointPolygonTest(bright_contour, pt, True)
                if dist > 0 and dist < max_neighbor_distance:
                    merged_bright = cv2.convexHull(np.concatenate((merged_bright, dark_contour)))
                    merge_flag = True
                    merged = True
                    break
            if not merge_flag:  # If the contour is not merged, add it to the updated dark contours list
                updated_dark_contours.append(dark_contour)
        dark_contours = updated_dark_contours  # Update dark_contours array after removing the merged contour
        if merged:
            merged_bright_contours.append(merged_bright)
        else:
            unmerged_bright_contours.append(bright_contour)

    unmerged_dark_contours = dark_contours
    return merged_bright_contours, unmerged_bright_contours, unmerged_dark_contours


def darkness(img, min_contour_area_threshold, max_contour_area_threshold):

    # make local copy of img for display purposes
    original = img

    # Adjust contrast and brightness levels in the grayscale image
    alpha = 10
    beta = 10
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # Apply sequence of thresholding and blurring
    img = cv2.GaussianBlur(img, (21, 21), 1000)
    # cv2.imshow("Original Input", img)
    # cv2.waitKey(0)
    _, img = cv2. threshold(img, 109, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Original Input", img)
    # cv2.waitKey(0)
    img = cv2.GaussianBlur(img, (81, 81), 1000)
    # cv2.imshow("Original Input", img)
    # cv2.waitKey(0)
    _, img = cv2. threshold(img, 130, 255, cv2.THRESH_BINARY)
    # cv2.imshow("Original Input", img)
    # cv2.waitKey(0)

    # Remove center artifact
    img[:,np.arange(1600,2400,dtype=int)] = 255

    # Canny Edge Detection
    edges_result = cv2.Canny(image=img, threshold1=100, threshold2=200)
    contours, _ = cv2.findContours(edges_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask image
    mask = np.zeros_like(edges_result)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

    # Dilate the mask to connect nearby regions to close the contour
    dilated_mask = cv2.dilate(mask, None, iterations=3)
    contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on size
    filtered_contours = [contour for contour in contours if min_contour_area_threshold <= cv2.contourArea(contour) <= max_contour_area_threshold]

    # Get number of landmarks detected
    num_landmarks = len(filtered_contours)
    # print("Number of Dark Landmarks:", num_landmarks)

    # Drawing the contours on the original image
    img_color = cv2.applyColorMap(original, cmap)    # Apply colormap
    img_with_dark_contours = img_color.copy()
    cv2.drawContours(img_with_dark_contours, filtered_contours, -1, (0, 255, 0), 2)  # Draw green contours
    return img_with_dark_contours, filtered_contours

def brightness(img, min_contour_area_threshold, max_contour_area_threshold):

    # make local copy of img for display purposes
    original = img

    # invert
    img = 255 - img

    # Adjust contrast and brightness levels in the inverted grayscale image
    alpha = 2.5
    beta = -120
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # Apply sequence of thresholding and blurring
    img = cv2.GaussianBlur(img, (51, 51), 1000)
    _, img = cv2. threshold(img, 245, 255, cv2.THRESH_BINARY)
    img = cv2.GaussianBlur(img, (81, 81), 1000)
    _, img = cv2. threshold(img, 170, 255, cv2.THRESH_BINARY)

    # Canny Edge Detection
    edges_result = cv2.Canny(image=img, threshold1=100, threshold2=200)
    contours, _ = cv2.findContours(edges_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask image
    mask = np.zeros_like(edges_result)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

    # Dilate the mask to connect nearby regions
    dilated_mask = cv2.dilate(mask, None, iterations=3)
    contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on size
    filtered_contours = [contour for contour in contours if min_contour_area_threshold <= cv2.contourArea(contour) <= max_contour_area_threshold]
    
    # Get number of landmarks
    num_landmarks = len(filtered_contours)
    # print("Number of Bright Landmarks:", num_landmarks)

    # Drawing the contours on the original image
    img_color = cv2.applyColorMap(original, cmap)
    img_with_bright_contours = img_color.copy()
    cv2.drawContours(img_with_bright_contours, filtered_contours, -1, (255, 0, 0), 2)  # Draw blue contours
    return img_with_bright_contours, filtered_contours

def get_contour_center(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0: # total area of contour
        cX = int(M["m10"] / M["m00"]) #sum of the x-coordinates of all pixels/total area of contour
        cY = int(M["m01"] / M["m00"]) #sum of the y-coordinates of all pixels/total area of contour
        return cX, cY
    else:
        return None



def adjust_coordinates(center, image_shape):
    center_x, center_y = center
    image_height, image_width = image_shape[:2]
    adjusted_center_x = center_x - image_width // 2
    adjusted_center_y = image_height // 2 - center_y  # Reversed due to image coordinates
    return adjusted_center_x, adjusted_center_y
    


def get_mpl_colormap(cmap_name):
    # Enables use of matplotlib colormaps, from https://stackoverflow.com/a/52501371
    cmap = plt.get_cmap(cmap_name)

    # Initialize the matplotlib color map
    sm = plt.cm.ScalarMappable(cmap=cmap)

    # Obtain linear color range
    color_range = sm.to_rgba(np.linspace(0, 1, 256), bytes=True)[:,2::-1]

    return color_range.reshape(256, 1, 3)



def downsample_sonar(linear_segment):
    ''' Downsamples sonar pings from 16-bit to 8-bit
    Returns a 2D numpy array with sonar data
    '''
    # Get data from sonar packets
    data_array = np.array([packet.data[0] for packet in linear_segment if packet.data[0].shape == (2000,)])
    data_array2 = np.array([packet.data[1] for packet in linear_segment if packet.data[1].shape == (2000,)])

    # Scale down the 16-bit values to 8-bit values
    scaled_data_array = ((data_array / 65535) * 255).astype(np.uint8)
    scaled_data_array2 = ((data_array2 / 65535) * 255).astype(np.uint8)

    # Concatenate port and stbd sonar pings
    downsampled_array = np.hstack((scaled_data_array, scaled_data_array2))

    return downsampled_array



cmap = get_mpl_colormap(plt.cm.copper)

def get_landmark_coordinates_segment(linear_segment, disp_images=False):
    '''Given a linear pass, returns landmark coordinates
    '''
    # Convert sonar data to 8-bit

    cmap = get_mpl_colormap(plt.cm.copper)

    downsampled_array = downsample_sonar(linear_segment)    # downsampled_array -> numpy array

    cmap = get_mpl_colormap(plt.cm.copper)
    if disp_images:
        img2_colored = cv2.applyColorMap(downsampled_array, cmap)
        cv2.imshow("Original Input", img2_colored)
        cv2.waitKey(0)

    min_dark_contour_area_threshold = 2500
    max_dark_contour_area_threshold = 200000
    dark_result, dark_contours = darkness(downsampled_array, min_dark_contour_area_threshold, max_dark_contour_area_threshold)

    min_bright_contour_area_threshold = 2500
    max_bright_contour_area_threshold = 100000
    bright_result, bright_contours = brightness(downsampled_array, min_bright_contour_area_threshold, max_bright_contour_area_threshold)

    # Merge contours
    max_neighbor_distance = 5000
    merged_bright_contours, unmerged_bright_contours, unmerged_dark_contours = merge_contours(bright_contours, dark_contours, max_neighbor_distance)

    # Combine all contours into a single list
    all_contours = merged_bright_contours + unmerged_bright_contours + unmerged_dark_contours

    # Filter contours based on minimum area threshold
    filtered_contours = [contour for contour in all_contours if cv2.contourArea(contour) >= 1000 and cv2.contourArea(contour) <= 200000]#570

    if disp_images:
        cv2.drawContours(img2_colored, filtered_contours, -1, (0, 255, 0), 2)  # Draw filtered contours

    midpoint = linear_segment[len(linear_segment)//2]

    lat0_value = midpoint.SensorXcoordinate
    lon0_value = midpoint.SensorYcoordinate
    heading_value = midpoint.SensorHeading      # Change this to use average heading over all passes
    pixelIToM_value = 0.1
    pixelJToM_value = 0.1

    frame_instance = frame(lat0_value, lon0_value, heading_value, pixelIToM_value, pixelJToM_value)

    # After merging contours and filtering them, iterate over each contour and get center coordinates
    landmark_coordinates = []

    for contour in filtered_contours:
        center = get_contour_center(contour)
        if center is not None:
            adjusted_center = adjust_coordinates(center, downsampled_array.shape)
            # print("Contour Center (Adjusted):",  adjusted_center)

            pixel_i, pixel_j = adjusted_center
            coordinate = tuple(reversed(frame_instance.pixelToGeo(pixel_i, pixel_j))) 
            # lat, lon = frame_instance.pixelToGeo(pixel_i, pixel_j)
            # print("Geographical Coordinates (Latitude, Longitude):", lat, lon)
        
            landmark_coordinates.append(coordinate)

            if disp_images:
                # Draw a circle at the contour center
                cv2.circle(img2_colored, center, 5, (0, 0, 255), -1)  # Red circle
        
    if disp_images:
        # Display the overlaid image with contour centers
        cv2.imshow('Overlayed Result with Contour Centers', img2_colored)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return landmark_coordinates

def get_landmark_coordinates(segmented_paths, disp_images=False):
    '''Gets all landmark coordinates
    Returns a list of coodinates
    '''
    landmark_coordinates = []
    for linear_segment in segmented_paths:
        landmark_coordinates.extend(get_landmark_coordinates_segment(linear_segment, disp_images=disp_images))

    return landmark_coordinates













