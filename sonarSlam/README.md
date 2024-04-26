# Senior_Design/sonarSlam
The files in this folder contain functions to read data from a directory of XTF (eXtended Triton Format) files. When used together, the files in this folder comprise the most complete form of our SLAM implementation for underwater robots. 

To run our package, clone the repository and run `cSlam.py`. `cSlam.py` takes in a required command line argument that is the directory containing xtf files on which our implementation should be run. There is a second optional argument that we call `plotting`. This is a boolean, and if set to true images of the landmark detection and relevant plots will be displayed as program moves through stages of execution. 

Example (no plotting):

`python cSlam.py '/path/to/xtfDirectory'`

Example (with plotting):

`python cSlam.py '/path/to/xtfDirectory' True`
