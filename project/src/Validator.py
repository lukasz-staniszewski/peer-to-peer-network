import hashlib

class Validator:
    def validate_hash(self, hash, data):
        hashed_data = hashlib.sha256(data)
        if hashed_data == hash:
            return True
        else:
            return False

    def create_hash(self, data):
        return hashlib.sha256(data)

