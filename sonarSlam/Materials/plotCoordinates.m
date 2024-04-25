% Read data from CSV file
data = readmatrix('new.csv');

% Extract X and Y coordinates
lon = data(:, 1);
lat = data(:, 2);

land = readgeotable("landareas.shp");
geoplot(land,FaceColor=[0.7 0.7 0.7],EdgeColor=[0.65 0.65 0.65])
hold on

% geoscatter(lat,lon,"filled")
geoplot(lat, lon, 'o', 'MarkerSize', 2, 'MarkerFaceColor', 'blue', 'MarkerEdgeColor', 'none');


a=min(lat);
b=max(lat);
c=min(lon);
d=max(lon);

geolimits([a b],[c d])

title('Palau WWII Torpedo Dump');