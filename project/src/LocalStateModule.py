class LocalStateModule:
    """
    Module representing local state.
    """
    def __init__(self):
        """
        Constructor of LocalStateModule.
        """
        self.my_files = []

    def get_myfiles_names(self):
        """
        Gets names of files from local state.

        :return: names of files from local state
        """
        names = [file.name for file in self.my_files]
        return names

    def add_local_file(self, file):
        """
        Adds given file to local state.

        :param file: name of file
        :return: true if added else false if duplicate
        """
        if file.name in self.get_myfiles_names():
            return False
        self.my_files.append(file)
        return True

    def remove_all_files(self):
        """
        Clears all files from local state.
        """
        self.my_files.clear()

    def remove_local_file(self, filename):
        """
        Removes file with given name from local state.

        :param filename: name of file to remove
        :return: true if performed else false if not found
        """
        if filename not in self.get_myfiles_names():
            return False
        self.my_files.remove(self.get_local_file(filename))
        return True

    def get_local_files(self):
        """
        Gets all files from local state.

        :return: all files
        """

        return self.my_files

    def get_local_file(self, filename):
        """
        Gets file object from local state if name of file suits.

        :param filename: name of file to find
        :return: file object if found else None
        """
        for file in self.my_files:
            if filename == file.name:
                return file
        return None
