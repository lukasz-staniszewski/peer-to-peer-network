class LocalStateModule:
    def __init__(self):
        self.my_files = []

    def get_myfiles_names(self):
        names = [file.name for file in self.my_files]
        return names

    def add_local_file(self, file):
        if file.name in self.get_myfiles_names():
            return False
        self.my_files.append(file)
        return True

    def remove_all_files(self):
        self.my_files.clear()

    def remove_local_file(self, filename):
        if filename not in self.get_myfiles_names():
            return False
        self.my_files.remove(self.get_local_file(filename))
        return True

    def get_local_files(self):
        return self.my_files

    def get_local_file(self, filename):
        for file in self.my_files:
            if filename == file.name:
                return file
        return None
