import pickle
from .Validator import Validator

class DataSerializer:
    def __init__(self):
        # CODE SMELL
        self.EOD = '\4'.encode()
        self.validator = Validator()

    def serialize_tcp(self, command, payload):
        data = pickle.dumps(payload) + self.EOD
        data_hash = self.validator.create_hash(data=data)
        serialized_msg = command.encode() + data_hash + data
        return serialized_msg

    def serialize_udp(self, command, payload):
        serialized_msg = command.encode() + pickle.dumps(payload) + self.EOD
        return serialized_msg

