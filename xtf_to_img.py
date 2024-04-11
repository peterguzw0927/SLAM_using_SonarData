import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pyxtf
import sunpy.visualization.colormaps as cm
import cv2


def get_mpl_colormap(cmap_name):
	# Enables use of matplotlib colormaps, from https://stackoverflow.com/a/52501371
    cmap = plt.get_cmap(cmap_name)

    # Initialize the matplotlib color map
    sm = plt.cm.ScalarMappable(cmap=cmap)

    # Obtain linear color range
    color_range = sm.to_rgba(np.linspace(0, 1, 256), bytes=True)[:,2::-1]

    return color_range.reshape(256, 1, 3)

def xtf_to_img():
    test_path = '../palau_files/20190122t024459z_leg015_survey_ss75.xtf'
    # test_path = '20130331083714H.xtf'
    (fh, packets) = pyxtf.xtf_read(test_path)

    # Get sonar pkts from xtf file
    sonar_packets = packets[pyxtf.XTFHeaderType.sonar]

    # Get data from sonar packets
    data_array = np.array([item.data[0] for item in sonar_packets])
    print(data_array.shape)
    data_array2 = np.array([item.data[1] for item in sonar_packets])

    # Scale down the 16-bit values to 8-bit values
    scale_factor = 1.2
    shift_factor = 20
    scaled_data_array = ((data_array / 65535) * 255 * scale_factor + shift_factor).astype(np.uint8)
    scaled_data_array2 = ((data_array2 / 65535) * 255 * scale_factor + shift_factor).astype(np.uint8)

    # Concatenate port and stbd sonar pings
    concatenated_array = np.hstack((scaled_data_array, scaled_data_array2))# + 20 	# Add shift to make image brighter

    # Confirm that values are 8-bit to work with OpenCV
    element_size = concatenated_array.itemsize * 8 	# mult. by 8 to go from bytes to bits
    print(f'Size of each element: {element_size} bits')

    # Plot sonar image
    # cmap = get_mpl_colormap(plt.cm.YlOrBr.reversed())
    # cmap = get_mpl_colormap(plt.cm.afmhot)
    # cmap = get_mpl_colormap(plt.cm.hot.reversed())
    # # cmap = get_mpl_colormap(matplotlib.colormaps['sdoaia171'])
    # imgg = cv2.applyColorMap(concatenated_array, cmap)#cv2.COLORMAP_HOT)
    imgg = concatenated_array
    
    return imgg
    # cv2.imshow('img', imgg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()