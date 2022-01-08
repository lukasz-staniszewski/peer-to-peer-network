import pickle


class DataDeserializer:

    def deserialize(self, data):
        command = data[0:4].decode().upper()
        payload = data[4:]
        payload = pickle.loads(payload)
        command = command.upper()
        return command, payload
