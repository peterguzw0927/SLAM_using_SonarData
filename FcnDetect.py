import cv2
import numpy as np
from pixeltogeo import frame

def process_image(image_path, min_dark_contour_area_threshold=200, max_dark_contour_area_threshold=2500,
                  min_bright_contour_area_threshold=260, max_bright_contour_area_threshold=1000,
                  max_neighbor_distance=5):
    
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
        # Convert the image to grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Adjust contrast and brightness levels in the grayscale image
        alpha = 17
        beta = 30
        high_contrast_result = cv2.convertScaleAbs(img_gray, alpha=alpha, beta=beta)
        img_blur = cv2.GaussianBlur(high_contrast_result, (7, 7), 0)

        # Canny Edge Detection
        edges_result = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
        contours, _ = cv2.findContours(edges_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a mask image
        mask = np.zeros_like(edges_result)
        cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

        # Dilate the mask to connect nearby regions to close the contour
        dilated_mask = cv2.dilate(mask, None, iterations=3)
        contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours = [contour for contour in contours if min_contour_area_threshold <= cv2.contourArea(contour) <= max_contour_area_threshold]
        num_landmarks = len(filtered_contours)
        print("Number of Dark Landmarks:", num_landmarks)

        # Drawing the contours on the original image
        img_with_dark_contours = img.copy()
        cv2.drawContours(img_with_dark_contours, filtered_contours, -1, (0, 255, 0), 2)  # Draw green contours
        return img_with_dark_contours, filtered_contours

    def brightness(img, min_contour_area_threshold, max_contour_area_threshold):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inverted_img_gray = 255 - img_gray

        # Adjust contrast and brightness levels in the inverted grayscale image
        alpha = 3.5
        beta = 40
        high_contrast_result = cv2.convertScaleAbs(inverted_img_gray, alpha=alpha, beta=beta)
        img_blur = cv2.GaussianBlur(high_contrast_result, (1, 1), 0)

        # Canny Edge Detection
        edges_result = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
        contours, _ = cv2.findContours(edges_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mask = np.zeros_like(edges_result)
        cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

        # Dilate the mask to connect nearby regions
        dilated_mask = cv2.dilate(mask, None, iterations=3)
        contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours = [contour for contour in contours if min_contour_area_threshold <= cv2.contourArea(contour) <= max_contour_area_threshold]
        num_landmarks = len(filtered_contours)
        print("Number of Bright Landmarks:", num_landmarks)

        # Drawing the contours on the original image
        img_with_bright_contours = img.copy()
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

    # Load image
    img = cv2.imread(image_path)

    # Apply darkness function
    dark_result, dark_contours = darkness(img, min_dark_contour_area_threshold, max_dark_contour_area_threshold)
    cv2.imshow('dark', dark_result)
    cv2.waitKey(0)

    # Apply brightness function
    bright_result, bright_contours = brightness(img, min_bright_contour_area_threshold, max_bright_contour_area_threshold)
    cv2.imshow('bright', bright_result)
    cv2.waitKey(0)

    # Merge contours
    merged_bright_contours, unmerged_bright_contours, unmerged_dark_contours = merge_contours(bright_contours, dark_contours, max_neighbor_distance)

    # Combine all contours into a single list
    all_contours = merged_bright_contours + unmerged_bright_contours + unmerged_dark_contours

    # Filter contours based on minimum area threshold
    filtered_contours = [contour for contour in all_contours if cv2.contourArea(contour) >= 570]
    overlaid_img = img.copy()
    num_landmarks = len(filtered_contours)
    print("Number of Landmarks:", num_landmarks)
    cv2.drawContours(overlaid_img, filtered_contours, -1, (0, 255, 0), 2)  # Draw filtered contours
    cv2.imshow('Overlayed Result', overlaid_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Define frame parameters
    lat0_value = 37.7749
    lon0_value = -122.4194
    heading_value = 45.0
    pixelIToM_value = 0.1
    pixelJToM_value = 0.1

    # Create frame instance
    frame_instance = frame(lat0_value, lon0_value, heading_value, pixelIToM_value, pixelJToM_value)

    # Process each contour
    for contour in filtered_contours:
        center = get_contour_center(contour)
        if center is not None:
            adjusted_center = adjust_coordinates(center, img.shape)
            print("Contour Center (Adjusted):", adjusted_center)

            pixel_i, pixel_j = adjusted_center
            lat, lon = frame_instance.pixelToGeo(pixel_i, pixel_j)
            print("Geographical Coordinates (Latitude, Longitude):", lat, lon)

            # Draw a circle at the contour center
            cv2.circle(overlaid_img, center, 5, (0, 0, 255), -1)  # Red circle

    # Display the overlaid image with contour centers
    cv2.imshow('Overlayed Result with Contour Centers', overlaid_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

