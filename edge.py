import cv2
import numpy as np

# Leer la imagen original
img = cv2.imread('190122F0005.jpg')
cv2.imshow('Image', img)
cv2.waitKey(0)

# Definir las coordenadas de la región de interés (ROI) centrada
height, width = img.shape[:2]
roi_x = width // 3
roi_y = height // 15
roi_width = width // 1
roi_height = height // 1

# Crear la región de interés (ROI)
roi = img[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
imgg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Ajustar los niveles de brillo en la parte izquierda de la imagen
alpha_non_roi = 4.0  # You can adjust this value according to your preference
beta_non_roi = 50    # You can adjust this value according to your preference

# Aplicar el ajuste de brillo a la parte izquierda de la imagen
imgg[:, :roi_x] = cv2.convertScaleAbs(imgg[:, :roi_x], alpha=alpha_non_roi, beta=beta_non_roi)
cv2.imshow('Img gray left part only changed', imgg)
cv2.waitKey(0)


# Ajustar los niveles de contraste y brillo en la imagen en escala de grises
alpha = 6.0
beta = 90
high_contrast_result = cv2.convertScaleAbs(imgg, alpha=alpha, beta=beta)
cv2.imshow('Img high contrast', high_contrast_result)
cv2.waitKey(0)


# Blur the high contrast grayscale image for better edge detection
img_blur = cv2.GaussianBlur(high_contrast_result, (7, 7), 0)

# Sobel Edge Detection
sobelx_result = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
sobely_result = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
sobelxy_result = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

# Display Sobel Edge Detection Images
cv2.imshow('Sobel X en Toda la Imagen', sobelx_result)
cv2.waitKey(0)
cv2.imshow('Sobel Y en Toda la Imagen', sobely_result)
cv2.waitKey(0)
cv2.imshow('Sobel X Y en Toda la Imagen usando Sobel()', sobelxy_result)
cv2.waitKey(0)

# Canny Edge Detection
edges_result = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)

# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection en Toda la Imagen', edges_result)
cv2.waitKey(0)

cv2.destroyAllWindows()
