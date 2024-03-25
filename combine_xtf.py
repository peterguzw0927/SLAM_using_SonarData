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
    print("File list: ", file_list)
    pings = []
    sorted_pings = []
    # Read each file
    for file in file_list:
        (fh, packets) = pyxtf.xtf_read(file)
        # Read add all sonar packets to a heap
        for packet in packets[pyxtf.XTFHeaderType.sonar]:
            heapq.heappush(pings, packet)

    print(fh)
    # Write the new pings to the output file
    with open(output_file, 'wb') as f:
        # Write file header
        f.write(fh.to_bytes())
        while pings:
            ping = heapq.heappop(pings)
            f.write(ping.to_bytes())
            sorted_pings.append(ping)
    
    np_chan1 = pyxtf.concatenate_channel(sorted_pings, file_header=fh, channel=0, weighted=True)
    np_chan2 = pyxtf.concatenate_channel(sorted_pings, file_header=fh, channel=1, weighted=True)
    
    upper_limit = 2 ** 40
    
    np_chan1.clip(0, upper_limit-1, out=np_chan1)
    np_chan2.clip(0, upper_limit-1, out=np_chan2)

    # The sonar data is logarithmic (dB), add small value to avoid log10(0)
    np_chan1 = np.log10(np_chan1 + 0.0001)
    np_chan2 = np.log10(np_chan2 + 0.0001)

    # Transpose so that the largest axis is horizontal
    np_chan1 = np_chan1 if np_chan1.shape[0] < np_chan1.shape[1] else np_chan1.T
    np_chan2 = np_chan2 if np_chan2.shape[0] < np_chan2.shape[1] else np_chan2.T

    # The following plots the waterfall-view in separate subplots
    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    # ax1.imshow(np_chan1, cmap='gray', vmin=0, vmax=np.log10(upper_limit))
    # ax2.imshow(np_chan2, cmap='gray', vmin=0, vmax=np.log10(upper_limit))
    # plt.show()

    merged_image = np.hstack((np_chan1, np_chan2))
    plt.figure(figsize=(12, 6))
    plt.imshow(merged_image, cmap='gray')
    plt.axis('off')  # Turn off axes
    plt.show()

    # Try reading the created file
    (file_header, packets) = pyxtf.xtf_read(output_file)
