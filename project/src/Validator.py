import hashlib


class Validator:
    """
    Class validator represents validator of sending hash.
    """
    def validate_hash(self, inp_hash, data):
        """
        Validates received hash with hash on received data.

        :param inp_hash: received hash
        :param data: received data
        :return: true if hashes are same else false
        """
        hashed_data = hashlib.sha256(data).digest()
        if hashed_data == inp_hash:
            return True
        else:
            return False

    def create_hash(self, data):
        """
        Creates hash on given data.

        :param data: data to hash
        :return: hash of given data
        """
        return hashlib.sha256(data).digest()
