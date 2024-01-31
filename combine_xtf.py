import pyxtf
import sys
import os



if __name__ == '__main__':
    scan_folder = sys.argv[1] # Directory of XTF sonar files to merge
    output_file = sys.argv[2] # name of the output file 
    
    # Get a list of xtf files
    file_list = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.xtf') and f != output_file] 
    print(file_list)
    
    pings = []
    file_header = None #Header for the new file
    
    # Read all sonar packets and store them in a single list
    for file in file_list:
        (file_header, packets) = pyxtf.xtf_read(file)
            
        for packet in packets[pyxtf.XTFHeaderType.sonar]:
            pings.append(packet)

    # Sort the list of packets by their ping number
    pings.sort(key=lambda x: x.PingNumber, reverse=False)
    
    for p in pings:
        print(p.Year, p.Month, p.Day, p.Hour, p.Minute, p.Second, p.PingNumber)
    print(pings[0])
    
    # Write the new pings to the output file
    with open(output_file, 'wb') as f:
        # Write file header
        f.write(file_header.to_bytes())

        for p in pings:
            f.write(p.to_bytes())
