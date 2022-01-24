import serial
from math import sqrt

class GetData:

    def __init__(self, port, baud):
        self.mag = serial.Serial(port=port, baudrate=baud)


    def get_raw_line(self):
        self.mag.read_all()
        raw_line = self.mag.readline().decode('ascii').split(',')
        return raw_line



    def perform_clean_exit(self):
        self.mag.close()