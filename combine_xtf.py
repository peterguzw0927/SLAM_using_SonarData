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
    output_file = sys.argv[2]
    # Get a list of xtf files
    file_list = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.xtf') and f != output_file] 
    #print(file_list)
    
    pings = []
    header_list = []
    # Read each file
    for file in file_list:
        (file_header, packets) = pyxtf.xtf_read(file)
        header_list.append(file_header)
        # Read add all sonar packets to a heap
        for packet in packets[pyxtf.XTFHeaderType.sonar]:
            heapq.heappush(pings,packet)
    
    fh = pyxtf.XTFFileHeader()
    fh.SonarName = b'TestWriter'
    fh.SonarType = pyxtf.XTFSonarType.unknown1
    fh.NavUnits = pyxtf.XTFNavUnits.latlon.value
    fh.NumberOfSonarChannels = 2
    
    # Port chaninfo
    fh.ChanInfo[0].TypeOfChannel = pyxtf.XTFChannelType.port.value
    fh.ChanInfo[0].SubChannelNumber = 0
    fh.ChanInfo[0].BytesPerSample = max(header_list, key=lambda x: x.ChanInfo[0].BytesPerSample).ChanInfo[0].BytesPerSample
    fh.ChanInfo[0].SampleFormat = pyxtf.XTFSampleFormat.byte.value
    # Stbd chaninfo
    fh.ChanInfo[1].TypeOfChannel = pyxtf.XTFChannelType.stbd.value
    fh.ChanInfo[1].SubChannelNumber = 1
    fh.ChanInfo[1].BytesPerSample = max(header_list, key=lambda x: x.ChanInfo[1].BytesPerSample).ChanInfo[1].BytesPerSample
    fh.ChanInfo[1].SampleFormat = pyxtf.XTFSampleFormat.byte.value
    
    # Write the new pings to the output file
    with open(output_file, 'wb') as f:
        # Write file header
        f.write(fh.to_bytes())
        for count in range(len(pings)):
            ping = heapq.heappop(pings)
            f.write(ping.to_bytes())
            #print(ping)
     # Try reading the created file
    #(file_header, packets) = pyxtf.xtf_read(output_file)
    
    # Print the heap in order
        #print(ping.Year, ping.Month, ping.Day, ping.Hour, ping.Minute, ping.Second, ping.PingNumber)

   
