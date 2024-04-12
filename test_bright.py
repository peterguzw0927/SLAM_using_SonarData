import cv2
import numpy as np
import pyxtf
import matplotlib.pyplot as plt
from pixeltogeo import frame
from xtfEdgeDetect import *


def local_brightness(img, min_contour_area_threshold, max_contour_area_threshold):

    original = img
    img = 255 - img

    # Adjust contrast and brightness levels in the inverted grayscale image
    alpha = 2.5
    beta = -120
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    img = cv2.GaussianBlur(img, (51, 51), 1000)
    _, img = cv2. threshold(img, 245, 255, cv2.THRESH_BINARY)
    img = cv2.GaussianBlur(img, (81, 81), 1000)
    _, img = cv2. threshold(img, 170, 255, cv2.THRESH_BINARY)


    cv2.imshow("blur", img)
    cv2.waitKey(0)

    # Canny Edge Detection
    edges_result = cv2.Canny(image=img, threshold1=100, threshold2=200)
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
    img_color = cv2.applyColorMap(original, cmap)
    img_with_bright_contours = img_color.copy()
    cv2.drawContours(img_with_bright_contours, filtered_contours, -1, (255, 0, 0), 2)  # Draw blue contours
    return img_with_bright_contours, filtered_contours

cmap = get_mpl_colormap(plt.cm.copper)

if __name__ == "__main__":
    # img = cv2.imread('CurlyTorpedo.jpg')
    path = '../palau_files/20190122t024459z_leg015_survey_ss75.xtf'
    img2 = read_xtf(path)
    cv2.imshow("Original Input", img2)
    cv2.waitKey(0)

    img2_colored = cv2.applyColorMap(img2, cmap)

    min_bright_contour_area_threshold = 2500 #260
    max_bright_contour_area_threshold = 100000 #1000
    bright_result, bright_contours = local_brightness(img2, min_bright_contour_area_threshold, max_bright_contour_area_threshold)
    cv2.imshow('bright', bright_result)
    cv2.waitKey(0)






