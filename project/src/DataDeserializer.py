import pickle


class DataDeserializer:

    def deserialize(self, data):
        command = data[0:4].decode().upper()
        payload = data[4:]
        payload = pickle.loads(payload)
        return command, payload
