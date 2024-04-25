'''
Read XTF files and sort sonar structs by timestamp


'''
import pyxtf
import numpy as np
import os

def get_xy_coordinates(packet):
    ''' Returns xy-coordinates for coordinate-based sorting
    This is currently unused
    '''
    return packet.SensorXcoordinate, packet.SensorYcoordinate

def get_timestamp(packet):
    ''' Returns timestamps for timestamp-based sorting
    '''
    return packet.Year, packet.Month, packet.Day, packet.Hour, packet.Minute, packet.Second, packet.HSeconds

def xtf_read_sort(directory):
    ''' Reads XTF files from a directory and sorts them
    Returns a list of sorted sonar structs
    '''
    sorted_structs = []

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path):    
            (fh, packets) = pyxtf.xtf_read(path)
            sonar_packets = packets[pyxtf.XTFHeaderType.sonar]
            sorted_structs.extend(sonar_packets)

    # Sort structs based on timestamp
    sorted_structs.sort(key=get_timestamp)

    return sorted_structs