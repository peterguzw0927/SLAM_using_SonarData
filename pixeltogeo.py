import math

class frame :
    ''' 
    Represents the coorindate system attached to one "frame" of sonar sidescan data.
    The frame is made of multiple scanlines that have been stacked to form an image.
    We assume the vehicle travels on a constant heading during the creation of this
    image.
    '''
    def __init__(self, lat0, lon0, heading, pixelIToM, pixelJToM) :
        '''
        Parameters:
          lat0: (deg) vehicle latitude at the center of the frame (i,j) == (0,0)
          lon0: (deg) vehicle longitude at the center of the frame (i,j) == (0,0)
          heading: (deg) vehicle heading during recording of frame
          pixelIToM: (m) width of each pixel in meters
          pixelJToM: (m) height of each pixel in meters
        '''
        self.lat0 = lat0
        self.lon0 = lon0
        self.heading = heading
        self.pixelCalI = pixelIToM
        self.pixelCalJ = pixelJToM
        nscale, escale = frame.northEastScale(lat0)
        r00, r01, r10, r11 = frame.rotation(heading)
        # The full transformation is diag(nscale, escale) * Rotation(heading) * diag(pixelJToM, pixelIToM)
        self.a00 = nscale*pixelJToM*r00
        self.a01 = nscale*pixelIToM*r01
        self.a10 = escale*pixelJToM*r10
        self.a11 = escale*pixelIToM*r11

    def pixelToGeo(self, deltaI, deltaJ) :
        ''' 
        Given a pixel at (deltaI, deltaJ) from the image center, compute that point's
        latitude & longitude in degrees
        '''
        dlat = self.a00 * deltaJ + self.a01 * deltaI
        dlon = self.a10 * deltaJ + self.a11 * deltaI
        lat = dlat + self.lat0
        lon = dlon + self.lon0
        return lat, lon

    def vehicleLocationAtSensing(self, deltaI, deltaJ) :
        '''
        When sensing an object at (deltaI, deltaJ), determine the location of the 
        vehicle. This assumes vehicle is at i == 0, j == deltaJ when it sensed objects
        along that row of pixels.
        '''
        return self.pixelToGeo(0, deltaJ)

    def rotation(heading) :
        '''
        Compute the rotation matrix from body to world
        '''
        psi = heading * math.pi/180.0
        c = math.cos(psi)
        s = math.sin(psi)
        r00 = c
        r01 = -s
        r10 = s
        r11 = c
        return r00, r01, r10, r11

    def northEastScale(lat0) :
        ''' 
        Compute the scale factor from meters north/east to
        degrees latitude/longitude
        '''
        # Compute the earth radius at lat0
        a = 6378137.0 # m
        b = 6356752.3 # m
        r2d = math.pi/180.0
    
        lat0r = lat0 * r2d
        coslat = math.cos(lat0r)
        sinlat = math.sin(lat0r)

        arg1 = math.pow(a * a * coslat, 2)
        arg2 = math.pow(b * b * sinlat, 2)
        arg3 = math.pow(a * coslat, 2)
        arg4 = math.pow(b * sinlat, 2)
        radius = math.sqrt((arg1 + arg2) / (arg3 + arg4));

        nscale = 1.0/ (r2d * radius)
        escale = 1.0 / (r2d * radius * coslat)
        return nscale, escale


