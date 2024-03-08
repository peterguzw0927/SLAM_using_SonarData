import numpy as np
import datetime
import heapq
import pyxtf
import sys
import os

# Get the unix timestamp of a packet
def get_packet_timestamp(x):
    return datetime.datetime(x.Year, x.Month, x.Day, x.Hour, x.Minute, x.Second, x.HSeconds).timestamp()

# Compare xtf packets by their unix timestamp
setattr(pyxtf.XTFPacket, "__lt__", lambda self, other: get_packet_timestamp(self) <= get_packet_timestamp(other))

if __name__ == '__main__':
    scan_folder = sys.argv[1] # Directory of XTF sonar files to merge
    output_file = sys.argv[2]
    # Get a list of xtf files
    file_list = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.xtf') and f != output_file] 
    print(file_list)
    pings = []

    # Read each file
    for file in file_list:
        (file_header, packets) = pyxtf.xtf_read(file)
        # Read add all sonar packets to a heap
        for packet in packets[pyxtf.XTFHeaderType.sonar]:
            heapq.heappush(pings, packet)
        
    print(file_header)
    # Write the new pings to the output file
    with open(output_file, 'wb') as f:
        # Write file header
        f.write(file_header.to_bytes())
        for p in pings:
            ping = heapq.heappop(pings)
            f.write(ping.to_bytes())
            #print(ping)
    
    # Try reading the created file
    (file_header, packets) = pyxtf.xtf_read(output_file)
        

   
