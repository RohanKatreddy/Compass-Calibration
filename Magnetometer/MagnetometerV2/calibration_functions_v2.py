import math

class CalibrationFunctions:

    def __init__(self, file_path):
        self.x = []
        self.y = []
        self.z = []
        self.max_magnitude = 0
        self.min_magnitude = 999
        self.max_magnitude_points = [0, 0]
        self.min_magnitude_points = [0, 0]
        self.file = open(file_path, 'r')


    def ellipse(self, shortest, longest, interval):
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

    def find_magnitudes(self, x, y):
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

    def retrive_data_from_file(self):
        for line in self.file:
            data = [float(value) for value in line.split(',')]
            if len(data) == 2:
                self.max_magnitude, self.min_magnitude = data
                continue
            if len(data) == 4:
                self.max_magnitude_points[0], self.max_magnitude_points[1] = data[0], data[1]
                self.min_magnitude_points[0], self.min_magnitude_points[1] = data[2], data[3]
                break
            self.x.append(data[0])
            self.y.append(data[1])
            self.z.append(data[2])
        #self.x, self.y = self.ellipse((-4, 1), (10, -1), 1)


    def calculate_offsets(self):
        self.x_offset = (max(self.x)+min(self.x))/2
        self.y_offset = (max(self.y)+min(self.y))/2
        self.max_magnitude, self.min_magnitude, self.max_magnitude_points, self.min_magnitude_points = self.find_magnitudes(self.x, self.y)


    def enforce_hard_iron_on_magnitudes(self):
        self.max_magnitude_points[0] += -(self.x_offset)
        self.max_magnitude_points[1] += -(self.y_offset)
        self.min_magnitude_points[0] += -(self.x_offset)
        self.min_magnitude_points[1] += -(self.y_offset)
        self.max_magnitude = math.sqrt(self.max_magnitude_points[0]**2 + self.max_magnitude_points[1]**2)
        self.min_magnitude = math.sqrt(self.min_magnitude_points[0]**2 + self.min_magnitude_points[1]**2)

    def enforce_hard_iron(self):
        for index in range(len(self.x)):
            self.x[index] = self.x[index] + -(self.x_offset)
            self.y[index] = self.y[index] + -(self.y_offset)

    def calculate_theta(self):
        self.theta = math.asin((self.max_magnitude_points[1] / self.max_magnitude))

    def calculate_rotation_matrix(self, theta):
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        return [(cos_theta, -sin_theta), ((sin_theta), cos_theta)]

    def calculate_scale_factor(self):
        self.scale_factor = self.min_magnitude/self.max_magnitude


    def enforce_rotation_matrix(self):
        rotation_matrix = self.calculate_rotation_matrix(self.theta)
        self.rotated_x_values, self.rotated_y_values = self.__enforce_rotation_matrix(rotation_matrix, self.x, self.y)

    def enforce_reverse_rotation_matrix(self):
        rotation_matrix = self.calculate_rotation_matrix(-self.theta)
        self.calibrated_x_values, self.calibrated_y_values = self.__enforce_rotation_matrix(rotation_matrix, self.rotated_x_values, self.rotated_y_values)

    def enforce_rotation_matrix_on_point(self, rotation_matrix, point):
        x = (rotation_matrix[0][0] * point[0]) + (rotation_matrix[0][1] * point[1])
        y = (rotation_matrix[1][0] * point[0]) + (rotation_matrix[1][1] * point[1])
        return x, y

    def __enforce_rotation_matrix(self, rotation_matrix, x_points, y_points):
        rotated_x_values, rotated_y_values = [], []
        for index in range(len(x_points)):
            x, y = self.enforce_rotation_matrix_on_point(rotation_matrix, [x_points[index], y_points[index]])
            rotated_x_values.append(x)
            rotated_y_values.append(y)
        return rotated_x_values, rotated_y_values


    def enforce_scale_factor(self):
        for index in range(len(self.rotated_x_values)):
            self.rotated_x_values[index] *= self.scale_factor

    def get_calibrated_values(self):
        return self.calibrated_x_values, self.calibrated_y_values

    def get_scale_factor(self):
        return self.scale_factor

    def get_offsets(self):
        return self.x_offset, self.y_offset

    def get_rotation_matrix(self):
        return self.calculate_rotation_matrix(self.theta), self.calculate_rotation_matrix(-self.theta)

    def get_calibrated_point(self, x, y, theta):
        x, y = self.enforce_rotation_matrix_on_point(self.calculate_rotation_matrix(theta), [x,y])
        x *= self.scale_factor
        x, y = self.enforce_rotation_matrix_on_point(self.calculate_rotation_matrix(-theta), [x,y])
        return x, y

    def set_scale_factor(self, s):
        self.scale_factor = s

    def get_theta(self):
        return self.theta