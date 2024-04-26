import sys

from make_graph import *
sys.path.append('../')
from process_XTF_files import xtf_read_sort
from nav_data import *
from landmark_detection import *

directory = "../../palau_files"
sonar_struct_list = xtf_read_sort(directory)

landmark_list = np.array(get_landmark_coordinates(segment_paths(sonar_struct_list), disp_images=False))

create_graph(sonar_struct_list, landmark_list=landmark_list, plot=True)