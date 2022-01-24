import pickle
from project.src.Validator import Validator


class DataSerializer:
    """
    Class represents data serializer.
    """
    def __init__(self):
        """
        DataSerializer constructor.
        """
        self.EOD = '\4'.encode()
        self.validator = Validator()

    def serialize_tcp(self, command, payload):
        """
        Performs serialization of tcp command and payload.

        :param command: command to serialize
        :param payload: payload to serialize
        :return: serialized message
        """
        data = pickle.dumps(payload) + self.EOD
        data_hash = self.validator.create_hash(data=data)
        serialized_msg = command.encode() + data_hash + data
        return serialized_msg

    def serialize_udp(self, command, payload):
        """
        Performs serialization of udp command and payload.

        :param command: command to serialize
        :param payload: payload to serialize
        :return: serialized message
        """
        serialized_msg = command.encode() + pickle.dumps(payload) + self.EOD
        return serialized_msg

