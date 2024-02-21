import datetime
import pyxtf
import sys
import os

if __name__ == '__main__':
    scan_folder = sys.argv[1] # Directory of XTF sonar files to merge
    
    # Get a list of xtf files
    file_list = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.xtf')] 
    print(file_list)
    
    pings = []
    packet_list = []
    
    # Read all sonar packets and store them in a single list
    for file in file_list:
        (file_header, packets) = pyxtf.xtf_read(file)
        
        #header_list.append(file_header)
        packet_list.append(packets)

        for packet in packets[pyxtf.XTFHeaderType.sonar]:
            pings.append(packet)
    

    # Sort the list of packets by their timestamp
    pings.sort(key=lambda x: datetime.datetime(x.Year, x.Month, x.Day, x.Hour, x.Minute, x.Second).timestamp(), reverse=False)


    for p in pings:
        print(p)
        #print(p.PingNumber, p.data)
        #print(p.Year, p.Month, p.Day, p.Hour, p.Minute, p.Second, p.PingNumber)
    #print(pings[0])
