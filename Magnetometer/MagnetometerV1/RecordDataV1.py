import serial
from math import sqrt

mag = serial.Serial(port='COM15', baudrate=9600)

def get_raw_data(mag):
    data = mag.readline().decode('ascii').split(',')
    return data


max_magnitude, min_magnitude = 0, 999
max_magnitude_points, min_magnitude_points = [0,0], [0,0]
data_file = open("C:\\Rohan\\Coding\\Python\\Projects\\AutonomousCarProject\\Magnetometer\\raw_mag_data.txt", 'w')

while True:

    try:
        raw_data = get_raw_data(mag) # Read mag data
        data_file.write((raw_data[0] + "," + raw_data[1] + "," + raw_data[2]).strip() + "\n"), # Write raw data to file
        magnitude = sqrt(float(raw_data[0])**2 + float(raw_data[1])**2) # Find the magnitude of the point

        # Check if its max magnitude
        if magnitude > max_magnitude:
            max_magnitude = magnitude
            max_magnitude_points[0], max_magnitude_points[1] = raw_data[0], raw_data[1]

        # Check if its min magnitude
        if magnitude < min_magnitude:
            min_magnitude = magnitude
            min_magnitude_points[0], min_magnitude_points[1] = raw_data[0], raw_data[1]

        mag.read_all() # clear serial buffer

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break

    except Exception as exception:
        print("Exception occured \n")
        print(exception)
        if input() == "q":
            break
        else:
            continue

data_file.write(str(max_magnitude) + "," + str(min_magnitude) + "\n")
data_file.write(str(max_magnitude_points) + "," + str(min_magnitude_points))
data_file.close()
mag.close()
print("Clean Exit")