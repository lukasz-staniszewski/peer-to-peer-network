class File:
    def __init__(self, filename, path):
        self.name = filename
        self.path = path

    def __repr__(self):
        return self.name

