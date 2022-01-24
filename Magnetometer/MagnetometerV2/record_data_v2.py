from format_data_v2 import FormatData
from get_data_v2 import GetData

class RecordData:

    def __init__(self, port, baud, path):
        try:
            self.mag = GetData(port, baud)
        except Exception as exception:
            print("check port and band of arduino")
            raise Exception(exception)
        try:
            self.file = open(path, 'w')
        except Exception as exception:
            print("check file path and make sure to use \\ like: folder\\subfolder")
            raise Exception(exception)
        self.format_data = FormatData(0, 999, self.file)

    def record_data(self):
        while True:

            try:
                raw_line = self.mag.get_raw_line()
                self.format_data.write_raw_line_to_file(raw_line)
                magnitude = self.format_data.get_magnitude(raw_line)
                self.format_data.check_for_max_magnitude(raw_line, magnitude)
                self.format_data.check_for_min_magnitude(raw_line, magnitude)
            except KeyboardInterrupt:
                print("Keyboard Interrupt")
                if input() == "q":
                    break
                else:
                    continue

            except Exception as exception:
                print("Exception occured:")
                print(exception)
                if input() == "q":
                    break
                else:
                    continue

        self.mag.perform_clean_exit()
        self.format_data.perform_clean_exit(self.file)