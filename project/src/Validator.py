import hashlib


class Validator:
    def validate_hash(self, inp_hash, data):
        hashed_data = hashlib.sha256(data).digest()
        if hashed_data == inp_hash:
            return True
        else:
            return False

    def create_hash(self, data):
        return hashlib.sha256(data).digest()
