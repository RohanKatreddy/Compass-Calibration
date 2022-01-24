from record_data_v2 import RecordData
from calibration_functions_v2 import CalibrationFunctions
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

file_path = "C:\\Rohan\\Coding\\Python\\Projects\\AutonomousCarProject\\Magnetometer\\MagnetometerV2\\raw_mag_data.txt"

mag = RecordData("COM15", 9600, file_path)

# COMMENT OUT ONCE USED PER MAGNETOMETER
mag.record_data()



calibration_functions = CalibrationFunctions(file_path)
calibration_functions.retrive_data_from_file()
calibration_functions.calculate_offsets()
calibration_functions.enforce_hard_iron_on_magnitudes()
calibration_functions.enforce_hard_iron()
calibration_functions.calculate_theta()
r, rr = calibration_functions.get_rotation_matrix()
x, y = calibration_functions.get_offsets()

calibration_functions.enforce_rotation_matrix()
calibration_functions.calculate_scale_factor()
s = calibration_functions.get_scale_factor()
calibration_functions.enforce_scale_factor()
calibration_functions.enforce_reverse_rotation_matrix()
t = calibration_functions.get_theta()

print(x, ", ", y)
print(r, ", ", rr)
print(s)
print(t)

x, y = calibration_functions.get_calibrated_values()
figure = plt.figure()
graph = plt.axes(projection ='3d')
graph.scatter(x, y)
graph.set_title("Magnetometer Raw Values")
plt.show()
