from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import math


def allign_major_axis_with_x_axis(R, x, y, scale_factor):
    rotated_x_values, rotated_y_values = [], []
    for index in range(len(x)):
        rotated_x_values.append(((R[0][0] * x[index]) + (R[0][1] * y[index]))*scale_factor)
        rotated_y_values.append((R[1][0] * x[index]) + (R[1][1] * y[index]))
    return rotated_x_values, rotated_y_values


def enforce_hard_iron(max_magnitude, min_magnitude, max_magnitude_points, min_magnitude_points, x, y, x_offset, y_offset):
    max_magnitude_points[0] += -(x_offset)
    max_magnitude_points[1] += -(y_offset)
    min_magnitude_points[0] += -(x_offset)
    min_magnitude_points[1] += -(y_offset)
    max_magnitude = math.sqrt(max_magnitude_points[0]**2 + max_magnitude_points[1]**2)
    min_magnitude = math.sqrt(min_magnitude_points[0]**2 + min_magnitude_points[1]**2)
    for i in range(len(x)):
        x[i] = x[i] + -(x_offset)
        y[i] = y[i] + -(y_offset)
    return max_magnitude, min_magnitude, max_magnitude_points, min_magnitude_points, x, y


def find_magnitudes(x, y):
    max_magnitude, min_magnitude = 0, 999
    max_magnitude_points, min_magnitude_points = [0,0], [0,0]
    for index in range(len(x)):
        radius = math.sqrt(x[index]**2 + y[index]**2)
        if radius > max_magnitude:
            max_magnitude = radius
            max_magnitude_points[0], max_magnitude_points[1] = x[index], y[index]
        elif radius < min_magnitude:
            min_magnitude = radius
            min_magnitude_points[0], min_magnitude_points[1] = x[index], y[index]
    return max_magnitude, min_magnitude, max_magnitude_points, min_magnitude_points


def ellipse(shortest, longest, interval):
    XValues, YValues = [], []
    x, y = 0, 1
    a = longest[x]/shortest[y]
    r = shortest[y]

    for i in range(-(longest[x]), longest[x]+1, interval):
        XValues.append(i)
        val = math.sqrt(r**2-(i/a)**2)
        YValues.append(val)
        XValues.append(i)
        YValues.append(-val)

    return XValues, YValues


data_file = open("C:\\Rohan\\Coding\\Python\\Projects\\AutonomousCarProject\\Magnetometer\\MagnetometerV2\\raw_mag_data.txt", 'r')

# Initialize variables
max_magnitude, min_magnitude = 0, 999
max_magnitude_points, min_magnitude_points = [0,0], [0,0]
rotated_x_values, rotated_y_values = [], []
calibrated_x_values, calibrated_y_values = [], []
x, y, z = [], [], []
x_offset, y_offset = 0, 0

for line in data_file:
    data = [float(value) for value in line.split(',')]
    if len(data) == 2:
        max_magnitude, min_magnitude = data
        continue
    if len(data) == 4:
        max_magnitude_points[0], max_magnitude_points[1] = data[0], data[1]
        min_magnitude_points[0], min_magnitude_points[1] = data[2], data[3]
        break
    x.append(data[0])
    y.append(data[1])
    z.append(data[2])
    x,y = ellipse((-4, 1), (10, -1), 1) # inserting ellipse coordinates to x and y lists


# Calculate offsets
x_offset = (max(x)+min(x))/2
y_offset = (max(y)+min(y))/2


# Enforce hard iron
max_magnitude, min_magnitude, max_magnitude_points, min_magnitude_points = find_magnitudes(x, y)
max_magnitude, min_magnitude, max_magnitude_points, min_magnitude_points, x, y = enforce_hard_iron(max_magnitude, min_magnitude, max_magnitude_points, min_magnitude_points, x, y, x_offset, y_offset)

# Calculate math values
theta = math.asin((max_magnitude_points[1] / max_magnitude))
cos_theta = math.cos(theta)
sin_theta = math.sin(theta)
R = [(cos_theta, -sin_theta), ((sin_theta), cos_theta)]
scale_factor = min_magnitude/max_magnitude
print(scale_factor)

# Calculate rotated ellipse points
rotated_x_values, rotated_y_values = allign_major_axis_with_x_axis(R, x, y, scale_factor)
print(min_magnitude, " ", max_magnitude)

# Rotate circle to starting point
cos_theta = math.cos(-theta)
sin_theta = math.sin(-theta)
R = [(cos_theta, sin_theta), (-(sin_theta), cos_theta)]
calibrated_x_values, calibrated_y_values = allign_major_axis_with_x_axis(R, rotated_x_values, rotated_y_values, 1)

# for i in range(len(x)):
#     x.append(calibrated_x_values[i] * 3)
#     y.append(calibrated_y_values[i] * 3)

x += calibrated_x_values
y += calibrated_y_values

print(max_magnitude_points)

figure = plt.figure()
graph = plt.axes(projection ='3d')
graph.scatter(x, y)
figure2 = plt.figure()
graph2 = plt.axes(projection ='3d')
graph2.scatter(calibrated_x_values, calibrated_y_values)
graph.set_title("Magnetometer Raw Values")
graph2.set_title("Magnetometer Raw Values2")
plt.show()