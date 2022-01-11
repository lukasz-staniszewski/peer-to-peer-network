class File:
    def __init__(self, filename, data):
        self.name = filename
        self.data = data

    def __repr__(self):
        return self.name

