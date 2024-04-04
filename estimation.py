import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from FcnDetect import process_image

def calculate_mean_and_covariance(landmark_data):
    all_landmarks = np.concatenate(landmark_data, axis=0)
    mean = np.mean(all_landmarks, axis=0)
    covariance = np.cov(all_landmarks.T)  # Ensure covariance is correctly calculated.
    return mean, covariance

def estimate_location_error(vehicle_location, mean, covariance):
    rv = multivariate_normal(mean, covariance)
    error_probability = rv.pdf(vehicle_location)
    return error_probability

def correct_vehicle_location(vehicle_location, mean, covariance):
    # Calculate the Mahalanobis distance
    delta = vehicle_location - mean
    mahalanobis_dist = np.sqrt(np.dot(np.dot(delta, np.linalg.inv(covariance)), delta.T))
    
    # Calculate the correction factor based on the Mahalanobis distance
    correction_factor = np.clip(1.0 - mahalanobis_dist / (2 * np.sqrt(2)), 0, 1)
    
    # Apply the correction
    corrected_location = vehicle_location + correction_factor * (mean - vehicle_location)
    return corrected_location

def calculate_mean_squared_error(vehicle_location, mean):
    squared_difference = (vehicle_location - mean) ** 2
    mse = np.mean(squared_difference)
    return mse

lat, long = process_image("CurlyTorpedo.jpg")

# Simulate observations and vehicle location
np.random.seed(42)
lat_array = np.array(lat)
long_array = np.array(long)

# Concatenate lat1 and long1 arrays along axis 1 (columns)
true_landmark_positions = np.concatenate((lat_array[:, np.newaxis], long_array[:, np.newaxis]), axis=1)

# Add observation noise to simulate visits
visit_1 = true_landmark_positions + np.random.normal(0, 0.00001, true_landmark_positions.shape)
#visit_2 = true_landmark_positions + np.random.normal(0, 0.0001, true_landmark_positions.shape)
#visit_3 = true_landmark_positions + np.random.normal(0, 0.0001, true_landmark_positions.shape)
#landmark_data = [visit_1, visit_2, visit_3]
print(true_landmark_positions.shape)
landmark_data = [true_landmark_positions,visit_1]
vehicle_location = np.array([37.7749, -122.4194])
vehicle_location2 = np.array([37.7748, -122.4192])
location = (vehicle_location + vehicle_location2)/2.0
heading = 45.0

# Calculate mean and covariance, then estimate error
mean, covariance = calculate_mean_and_covariance(landmark_data)
error_probability = estimate_location_error(location, mean, covariance)

# Now, apply the correction
corrected_location = correct_vehicle_location(location, mean, covariance)

#print(f"Vehicle Location Error Probability: {error_probability}")
print(f"Corrected Vehicle Location: {corrected_location}")

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot original landmark positions
ax.scatter(true_landmark_positions[:, 1], true_landmark_positions[:, 0], np.zeros_like(true_landmark_positions[:, 0]), color='blue', label='Landmarks (1st visit)')

# Plot observed landmark positions
ax.scatter(visit_1[:, 1], visit_1[:, 0], np.zeros_like(visit_1[:, 0]), color='green', alpha=0.5, label='Landmarks (2nd visit)')

# Plot original vehicle location
ax.scatter(vehicle_location[1], vehicle_location[0], 0, color='red', label='Vehicle location (1st visit)')
ax.scatter(vehicle_location2[1], vehicle_location2[0], 0, color='purple', label='Vehicle location (2nd visit)')

# Plot corrected vehicle location
ax.scatter(corrected_location[1], corrected_location[0], 0, color='orange', label='Corrected Vehicle Location')

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Depth')

plt.title('Landmarks and Vehicle Locations')
plt.legend()
plt.grid(True)
plt.show()

# Calculate Mean Squared Error
mse = calculate_mean_squared_error(vehicle_location, mean)
print(f"Mean Squared Error: {mse}")
