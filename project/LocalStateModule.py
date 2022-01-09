class LocalStateModule:

    def add_local_file(self, filename, my_files):
        files = my_files['files']
        if filename in files:
            return False
        files.append(filename)
        my_files['files'] = files
        # Wyslij BROADCAST, ze dodalem plik --> 'NWRS' + UDP_STR_RS
        port = TCP_PORT

        struc = UDP_STR_RS(address, port, filename)
        struc_pickled = pickle.dumps(struc)

        command = 'NWRS'.encode()
        print(f'SENDING NWRS, filename: {filename}')
        send_broadcast(command + struc_pickled)
        return True


    def remove_local_file(filename, my_files):
        files = my_files['files']
        if filename not in files:
            return False
        files.remove(filename)
        my_files['files'] = files
        # Wyslij BROADCAST, ze usunalem plik --> 'RMRS' + UDP_STR_RS
        address = my_files['address']
        port = my_files['udp_port']

        struc = UDP_STR_RS(address, filename, port)
        struc_pickled = pickle.dumps(struc)

        command = 'RMRS'.encode()
        print(f'SENDING RMRS, filename: {filename}')
        send_broadcast(command + struc_pickled)