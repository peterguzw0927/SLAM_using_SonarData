# Our initial 2D slam model in first semester 

In this project we gather data from sensing of generated landmarks then calculate it's position in a 2d world. This process is repeated every time we move to have an understanding of the robots localization in this enviroment. Graph SLAM is the method used, it simplifies the estimation by defining the probabilities using a sequence of constraints. It takes in its initial position and then calculates based on previous poses to a newer pose.

![download](https://github.com/peterguzw0927/Senior_Design/assets/114111503/01e988cf-79d6-4489-85ce-e23a7e4e30a8)

The Xs are the potential landmarks and the red o is our UUV.

The data that is generated is random, but you did specify the number, N, or time steps that the robot was expected to move and the num_landmarks in the world (which your implementation of slam should see and estimate a position for. Your robot should also start with an estimated pose in the very center of your square world, whose size is defined by world_size.

Finally, using the display_world code from the helpers.py file (which was also used in the first notebook), we can actually visualize what you have coded with slam: the final position of the robot and the positon of landmarks, created from only motion and measurement data!

Output is going to look like this:

Estimated Poses:

[50.000, 50.000]
[37.973, 33.652]
[26.185, 18.155]
[13.745, 2.116]
[28.097, 16.783]
[42.384, 30.902]
[55.831, 44.497]
[70.857, 59.699]
[85.697, 75.543]
[74.011, 92.434]
[53.544, 96.454]
[34.525, 100.080]
[48.623, 83.953]
[60.197, 68.107]
[73.778, 52.935]
[87.132, 38.538]
[80.303, 20.508]
[72.798, 2.945]
[55.245, 13.255]
[37.416, 22.317]


Estimated Landmarks:
[82.956, 13.539]
[70.495, 74.141]
[36.740, 61.281]
[18.698, 66.060]
[20.635, 16.875]
