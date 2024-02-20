import pyxtf
import sys
import os
import datetime
import time

if __name__ == '__main__':
    scan_folder = sys.argv[1] # Directory of XTF sonar files to merge
    #output_file = sys.argv[2] # name of the output file 
    
    # Get a list of xtf files
    file_list = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.xtf')] 
    print(file_list)
    
    pings = []
    #header_list = []
    packet_list = []
    # Read all sonar packets and store them in a single list
    for file in file_list:
        (file_header, packets) = pyxtf.xtf_read(file)
        
        #header_list.append(file_header)
        packet_list.append(packets)

        for packet in packets[pyxtf.XTFHeaderType.sonar]:
            pings.append(packet)
    
    # Initialize file header
    """
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
    """

    # Sort the list of packets by their ping number
    pings.sort(key=lambda x: time.mktime(datetime.datetime(x.Year, x.Month, x.Day, x.Hour, x.Minute).timetuple()) + x.Second, reverse=False)


    for p in pings:
        print(p.PingNumber, p.data)
        #print(p.Year, p.Month, p.Day, p.Hour, p.Minute, p.Second, p.PingNumber)
    #print(pings[0])
    """
    # Write the new pings to the output file
    with open(output_file, 'wb') as f:
        # Write file header
        f.write(fh.to_bytes())

        for p in pings:
            f.write(p.to_bytes())


    # Try reading the created file
    (file_header, packets) = pyxtf.xtf_read(output_file)
    """
