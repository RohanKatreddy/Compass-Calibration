from math import sqrt

class FormatData:

    def __init__(self, max_magnitude, min_magnitude, file):
        self.file = file
        self.max_magnitude = max_magnitude
        self.min_magnitude = min_magnitude
        self.max_magnitude_points = [0,0]
        self.min_magnitude_points = [0,0]

    def write_raw_line_to_file(self, raw_line):
        self.file.write((raw_line[0] + "," + raw_line[1] + "," + raw_line[2]).strip() + "\n")


    @staticmethod
    def get_magnitude(raw_line):
        return sqrt(float(raw_line[0])**2 + float(raw_line[1])**2)

    def check_for_max_magnitude(self, raw_line, magnitude):
        if magnitude > self.max_magnitude:
                self.max_magnitude = magnitude
                self.max_magnitude_points = raw_line[0], raw_line[1]

    def check_for_min_magnitude(self, raw_line, magnitude):
        if magnitude < self.min_magnitude:
                    self.min_magnitude = magnitude
                    self.min_magnitude_points = raw_line[0], raw_line[1]

    def perform_clean_exit(self, file):
        file.write(str(self.max_magnitude) + "," + str(self.min_magnitude) + "\n")
        file.write(str(self.max_magnitude_points) + "," + str(self.min_magnitude_points))
        file.close()