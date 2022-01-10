class LocalStateModule:
    def __init__(self):
        self.my_files = []

    def add_local_file(self, filename):
        if filename in self.my_files:
            return False
        self.my_files.append(filename)
        # Wyslij BROADCAST, ze dodalem plik --> 'NWRS' + UDP_STR_RS -> coordynator
        return True

    def remove_local_file(self, filename):
        if filename not in self.my_files:
            return False
        self.my_files.remove(filename)
        # Wyslij BROADCAST, ze usunalem plik --> 'RMRS' + UDP_STR_RS -> coordynator
        return True

    def get_local_files(self):
        return self.my_files
