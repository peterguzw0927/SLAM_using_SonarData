import cv2
from FcnDetect import process_image
from ReadSonar import plot_xtf
import tempfile
import os

if __name__ == "__main__":
    file_path = "20130328231349L.xtf"
    merged_image = plot_xtf(file_path)
    
    # Save the merged image to a temporary file
    temp_dir = tempfile.gettempdir()
    temp_image_path = os.path.join(temp_dir, "merged_image.png")
    cv2.imwrite(temp_image_path, merged_image)
    process_image(temp_image_path)
    
