import pickle


class DataSerializer:
    def __init__(self):
        self.EOD = '\4'.encode()

    def serialize_msg(self, command, payload):
        serialized_msg = command.encode() + pickle.dumps(payload) + self.EOD
        return serialized_msg
