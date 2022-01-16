class RemoteStateModule:
    def __init__(self):
        self.others_files = {}

    def add_to_others_files(self, filename, address, port):
        if filename in self.others_files.keys():
            curr_files = self.others_files[filename]
            if (address, port) not in self.others_files[filename]:
                curr_files.append((address, port))
            self.others_files[filename] = curr_files
        else:
            self.others_files[filename] = [(address, port)]

    def remove_from_others_files(self, filename, address, port):
        for key, value in self.others_files.items():
            if key.name == filename:
                if len(self.others_files[key]) == 1:
                    self.others_files.pop(key)
                    return True
                else:
                    curr_files = self.others_files[key]
                    curr_files.remove((address, port))
                    self.others_files[key] = curr_files
                    return True
        return False

    def remove_node_from_others_files(self, address, port):
        keys_to_delete = []
        for key, val in self.others_files.items():
            print(f'INFO | REMOTE STATE | Want to remove: {(address, port)}')
            if (address, port) in val:
                if len(val) == 1:
                    keys_to_delete.append(key)
                else:
                    val.remove((address, port))
                print(f'INFO | REMOTE STATE | removing {(address, port)}')

        for key in keys_to_delete:
            self.others_files.pop(key)

    def get_addresses_by_filename(self, filename):
        for key, value in self.others_files.items():
            if key.name == filename:
                return value

