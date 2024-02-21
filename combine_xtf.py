import datetime
import heapq
import pyxtf
import sys
import os

# Get the unix timestamp of a packet
def get_packet_timestamp(x):
    return datetime.datetime(x.Year, x.Month, x.Day, x.Hour, x.Minute, x.Second).timestamp()

# Compare xtf packets by their unix timestamp
setattr(pyxtf.XTFPacket, "__lt__", lambda self, other: get_packet_timestamp(self) <= get_packet_timestamp(other))



if __name__ == '__main__':
    scan_folder = sys.argv[1] # Directory of XTF sonar files to merge
    
    # Get a list of xtf files
    file_list = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.xtf')] 
    #print(file_list)
    
    pings = []
    # Read all sonar packets and store them in a heap
    for file in file_list:
        (file_header, packets) = pyxtf.xtf_read(file)
        
        for packet in packets[pyxtf.XTFHeaderType.sonar]:
            heapq.heappush(pings,packet)

    # Print the heap in order 
    for count in range(len(pings)):
        ping = heapq.heappop(pings)
        print(ping)
        #print(ping.Year, ping.Month, ping.Day, ping.Hour, ping.Minute, ping.Second, ping.PingNumber)
    #print(pings[0])
