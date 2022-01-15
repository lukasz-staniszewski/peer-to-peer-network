import pickle
from Validator import Validator


class DataDeserializer:

    def __init__(self):
        self.validator = Validator()

    def deserialize_tcp(self, data):
        command = data[0:4].decode().upper()
        hash = data[4:36]
        payload = data[36:]

        if self.validator.validate_hash(hash=hash, data=payload):
            try:
                payload = pickle.loads(payload)
            except pickle.UnpicklingError:
                raise Exception("Deserialization pickle error")
            return command, payload
        else:
            raise Exception("Deserialization found hash not correct")

    def deserialize_udp(self, data):
        command = data[0:4].decode().upper()
        payload = data[4:]
        payload = pickle.loads(payload)
        return command, payload
