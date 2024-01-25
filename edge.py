import cv2

# Leer la imagen original
img = cv2.imread('20190122_SCOUT.tif')

# Display original image
cv2.imshow('Original', img)
cv2.waitKey(0)

# Convertir a escala de grises
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Ajustar los niveles de contraste para hacer la escala de grises más exagerada
alpha = 2  # Factor de escala
beta = 50    # Factor de desplazamiento
exaggerated_gray = cv2.convertScaleAbs(img_gray, alpha=alpha, beta=beta)

# Mostrar la imagen original y la imagen con escala de grises exagerada
cv2.imshow('Original Grayscale', img_gray)
cv2.imshow('Exaggerated Grayscale', exaggerated_gray)
cv2.waitKey(0)

# Blur the exaggerated grayscale image for better edge detection
img_blur = cv2.GaussianBlur(exaggerated_gray, (7,7), 0)

# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

# Display Sobel Edge Detection Images
cv2.imshow('Sobel X', sobelx)
cv2.waitKey(0)
cv2.imshow('Sobel Y', sobely)
cv2.waitKey(0)
cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
cv2.waitKey(0)

# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', edges)
cv2.waitKey(0)

cv2.destroyAllWindows()