import configparser
import os


class FileCoordinator:
    """
    Class represents coordinator of files on disk.
    """
    def __init__(self):
        """
        FileCoordinator constructor.
        """
        config = configparser.ConfigParser()
        config.read("project/conf_log/conf.ini")
        self.files_folder_path = config['COORDINATOR']['file_path']

    def save_to_file(self, file_name, file_data):
        """
        Performs saving data to disk.

        :param file_name: name of new file on disk
        :param file_data: data for new file
        :return: path to new file
        """
        with open(self.files_folder_path + file_name, "wb+") as file:
            file.write(file_data)
        return self.files_folder_path + file_name

    def get_data_from_file(self, file_path):
        """
        Gets file in bytes from disk.

        :param file_path: path on disk to file
        """
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                data = file.read()
            return data
        else:
            return False
