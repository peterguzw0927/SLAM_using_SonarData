import cv2
import numpy as np
import pyxtf
import matplotlib.pyplot as plt
from pixeltogeo import frame
from xtfEdgeDetect import *


def local_brightness(img, min_contour_area_threshold, max_contour_area_threshold):

    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = img
    inverted_img_gray = 255 - img_gray

    # Adjust contrast and brightness levels in the inverted grayscale image
    alpha = 2.5
    beta = 20
    high_contrast_result = cv2.convertScaleAbs(inverted_img_gray, alpha=alpha, beta=beta)
    img_blur = cv2.GaussianBlur(high_contrast_result, (1, 1), 0)

    cv2.imshow("blur", img_blur)
    cv2.waitKey(0)

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


    # Merging contours
    merged_contours = merge_contours(contours, contours, max_neighbor_distance=10)
    filtered_contours = merged_contours

    # Drawing the contours on the original image
    img_color = cv2.applyColorMap(img_gray, cmap)
    img_with_bright_contours = img_color.copy()
    cv2.drawContours(img_with_bright_contours, filtered_contours, -1, (255, 0, 0), 2)  # Draw blue contours
    return img_with_bright_contours, filtered_contours


if __name__ == "__main__":
    # img = cv2.imread('CurlyTorpedo.jpg')
    path = '../palau_files/20190122t024459z_leg015_survey_ss75.xtf'
    img2 = read_xtf(path)
    cv2.imshow("Original Input", img2)
    cv2.waitKey(0)

    img2_colored = cv2.applyColorMap(img2, cmap)

    min_bright_contour_area_threshold = 260 #260
    max_bright_contour_area_threshold = 1000 #1000
    bright_result, bright_contours = local_brightness(img2, min_bright_contour_area_threshold, max_bright_contour_area_threshold)
    cv2.imshow('bright', bright_result)
    cv2.waitKey(0)






