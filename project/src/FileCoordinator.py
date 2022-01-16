import configparser
import os


class FileCoordinator:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("conf_log/conf.ini")
        self.files_folder_path = config['COORDINATOR']['file_path']

    def save_to_file(self, file_name, file_data):
        with open(self.files_folder_path + file_name, "wb+") as file:
            file.write(file_data)
        return self.files_folder_path + file_name

    def get_data_from_file(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                data = file.read()
            return data
        else:
            return False
