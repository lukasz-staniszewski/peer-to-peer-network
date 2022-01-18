import logging


class RemoteStateModule:
    """
    Module represents remote state.
    """
    def __init__(self):
        """
        Constructor of RemoteStateModule.
        """
        self.others_files = {}

    def add_to_others_files(self, filename, address, port):
        """
        Function adds given file name to remote states.

        :param filename: name of file
        :param address: address from which file is
        :param port: port from which file is
        """
        if str(filename) in self.others_files.keys():
            curr_files = self.others_files[filename]
            if (address, port) not in self.others_files[filename]:
                curr_files.append((address, port))
            self.others_files[filename] = curr_files
        else:
            self.others_files[filename] = [(address, port)]

    def remove_from_others_files(self, filename, address, port):
        """
        Removes given node from given file name owners group.

        :param filename: name of file
        :param address: address of node
        :param port: port of node
        :return: true if such file exists in remote state else false
        """
        for key, value in self.others_files.items():
            if key == filename:
                if len(self.others_files[key]) == 1:
                    self.others_files.pop(key)
                else:
                    curr_files = self.others_files[key]
                    curr_files.remove((address, port))
                    self.others_files[key] = curr_files
                return True
        return False

    def remove_node_from_others_files(self, address, port):
        """
        Removes node from each file which he was sharing in remote state.

        :param address: address of node
        :param port: port of node
        """
        keys_to_delete = []
        for key, val in self.others_files.items():
            logging.info(f'REMOTE STATE | Want to remove: {(address, port)}')
            if (address, port) in val:
                if len(val) == 1:
                    keys_to_delete.append(key)
                else:
                    val.remove((address, port))
                print(f'INFO | From remote state removing {(address, port)}')
                logging.info(f'REMOTE STATE | removing {(address, port)}')

        for key in keys_to_delete:
            self.others_files.pop(key)

    def get_addresses_by_filename(self, filename):
        """
        Returns addresses of all nodes that shares file with given name.
        :param filename: name of file
        :return: addressess of nodes
        """
        for key, value in self.others_files.items():
            if key == filename:
                return value

