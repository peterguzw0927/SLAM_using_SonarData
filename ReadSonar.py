import pyxtf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Read the test file
# Note that at this point, the header_7125 and header_7125_snippet is not implemented, which is why a warning is shown
# The bathymetry and sonar headers are implemented, however - which can be read while ignoring the unimplemented packets
test_file = "20130331083714L.xtf"
(fh, p) = pyxtf.xtf_read(test_file)

# This prints all the ctypes fields present
#print(fh)

# The ChanInfo field is an array of XTFChanInfo objects
# Note that the ChanInfo field always has a size of 6, even if the number of channels is less. 
# Use the fh.NumXChannels fields to calculate the number (the function xtf_channel_count does this)
n_channels = fh.channel_count(verbose=True)
actual_chan_info = [fh.ChanInfo[i] for i in range(0, n_channels)]
#print('Number of data channels: {}\n'.format(n_channels))

# Print the first channel
#print(actual_chan_info[0])

# Print the keys in the packets-dictionary
#print([key for key in p])

# The returned packets is a Dict[XTFHeaderType, List[XTFClass]]
# The values in the dict are lists of pings, of the class in question
sonar_ch = p[pyxtf.XTFHeaderType.sonar]  # type: List[pyxtf.XTFPingHeader]

# Each element in the list is a ping (XTFPingHeader)
# This retrieves the first ping in the file of the sonar type
sonar_ch_ping1 = sonar_ch[0]

# The properties in the header defines the attributes common for all subchannels 
# (e.g sonar often has port/stbd subchannels)
print(sonar_ch_ping1)

# The data and header for each subchannel is contained in the data and ping_chan_headers respectively.
# The data is a list of numpy arrays (one for each subchannel)
sonar_subchan0 = sonar_ch_ping1.data[0]  # type: np.ndarray
sonar_subchan1 = sonar_ch_ping1.data[1]  # type: np.ndarray
#print(sonar_subchan0)

# print(sonar_subchan0.shape)
# print(sonar_subchan1.shape)
#print(sonar_subchan0)
#print(sonar_ch_ping1.data[0])
#sonar_subchan0 = sonar_ch_ping1.data[0]
#print(sonar_subchan0)

#fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
#ax1.semilogy(np.arange(0, sonar_subchan0.shape[0]), sonar_subchan0)
#ax2.semilogy(np.arange(0, sonar_subchan1.shape[0]), sonar_subchan1)
#plt.show()

# Each subchannel has a XTFPingChanHeader, 
# which contains information that can change from ping to ping in each of the subchannels
sonar_ping1_ch_header0 = sonar_ch_ping1.ping_chan_headers[0]
#print(sonar_ping1_ch_header0)

# The function concatenate_channels concatenates all the individual pings for a channel, and returns it as a dense numpy array
np_chan1 = pyxtf.concatenate_channel(p[pyxtf.XTFHeaderType.sonar], file_header=fh, channel=0, weighted=True)
np_chan2 = pyxtf.concatenate_channel(p[pyxtf.XTFHeaderType.sonar], file_header=fh, channel=1, weighted=True)

# Clip to range (max cannot be used due to outliers)
# More robust methods are possible (through histograms / statistical outlier removal)
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

# # Merge the two images horizontally
# # Convert grayscale images to RGB
# np_chan1_rgb = cm.gray(np_chan1 / np.max(np_chan1))[:, :, :3]
# np_chan2_rgb = cm.gray(np_chan2 / np.max(np_chan2))[:, :, :3]

# # Merge the two RGB images horizontally
# merged_image_rgb = np.hstack((np_chan1_rgb, np_chan2_rgb))