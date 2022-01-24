import math
from calibration_functions_v2 import CalibrationFunctions

file_path = "C:\\Rohan\\Coding\\Python\\Projects\\AutonomousCarProject\\Magnetometer\\MagnetometerV2\\raw_mag_data.txt"

#mag = RecordData("COM15", 9600, file_path)

# COMMENT OUT ONCE USED PER MAGNETOMETER
#mag.record_data()



calibration_functions = CalibrationFunctions(file_path)
x, y = 21.41,-0.77
h = math.atan2(y, x)
print(h)
if h < 0:
    h += 2*math.pi
if h > 2*math.pi:
    h -= 2*math.pi

d = 360 - (h * (180/math.pi))
print(d)

calibration_functions.set_scale_factor(0.9754276949285907)
x, y = calibration_functions.get_calibrated_point(x, y, -1.1900399184338348)
print(x, ", ", y)

print(math.degrees(math.atan2(y, x)))