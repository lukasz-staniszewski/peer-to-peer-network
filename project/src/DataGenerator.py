class DataGenerator:

    def generate_data(self, data_len):
        data = "".join([str(chr((i % 26) + 65)) for i in range(data_len)])
        return data
