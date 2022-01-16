import threading
import socket
import logging
import ast
from project.src.Coordinator import remote_state_lock

# UDP_PORT = 8888
# BUFFER_SIZE = 1024
# UDP_PERMITTED_MESS = ['GETS', 'NWRS', 'RMRS', 'NORS', 'SKIP']


class UDPModule:

    def __init__(self, address,  udp_port, buffer_size, permitted_cmds):
        self.port = udp_port
        self.buffer_size = buffer_size
        self.address = address
        self.permitted_messages = ast.literal_eval(permitted_cmds)
        self.udp_socket = None

    def create_and_bind_udp_listener(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))
        return sock

    def send_broadcast(self, message):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.sendto(message, ('<broadcast>', self.port))
        # print("INFO | SERVER UDP | Broadcast sent!")
        logging.info("SERVER UDP | Broadcast sent!")

    def udp_listener(self, coordinator):
        # print('INFO | SERVER UDP | UDP Listener is running')
        logging.info("SERVER UDP | UDP Listener is running")
        while True:
            message = self.udp_socket.recv(self.buffer_size)
            command, payload = coordinator.deserialize_udp(message)
            # ignoring own broadcast
            if payload.ip_address == self.address:
                command = 'SKIP'
                # print('INFO | SERVER UDP | Ignoring own broadcast!')
                logging.info("SERVER UDP | Ignoring own broadcast!")

            # send your list to node
            elif command == 'GETS':
                # print('INFO | SERVER UDP | GOT GETS BROADCAST!')
                logging.info("SERVER UDP | GOT GETS BROADCAST!")
                add = payload.ip_address
                port = payload.port
                # sending my_files on specific address
                try:
                    coordinator.send_ndst(add, port)
                except Exception as exception:
                    print(f'ERROR | Failed to send data!')
                    logging.warning(f"SERVER UDP | Failed to send data -> {exception}")

            # node share new file
            elif command == 'NWRS':
                # print('INFO | SERVER UDP | GOT NWRS BROADCAST!')
                logging.info(f"SERVER UDP | GOT NWRS BROADCAST!")
                address = payload.ip_address
                port = payload.port
                filename = payload.file_name
                with remote_state_lock:
                    coordinator.remote_state.add_to_others_files(filename, address, port)
                print(f'INFO | Adding owner of file: {filename}')
                logging.info(f"SERVER UDP | GOT NWRS BROADCAST | Uploaded: {filename}")

            #remove assigned node to specific file
            elif command == 'RMRS':
                address = payload.ip_address
                port = payload.port
                filename = payload.file_name
                with remote_state_lock:
                    coordinator.remote_state.remove_from_others_files(filename, address, port)
                print(f'INFO | Deleted owner of file: {filename}')
                logging.info(f"SERVER UDP | GOT RMRS BROADCAST | Deleted: {filename}")

            # node is now not sharing any files
            elif command == 'NORS':
                # print(f'INFO | SERVER UDP | GOT NORS BROADCAST')
                logging.info(f"SERVER UDP | GOT NORS BROADCAST")
                address = payload.ip_address
                port = payload.port
                with remote_state_lock:
                    coordinator.remote_state.remove_node_from_others_files(address, port)

            if command not in self.permitted_messages:
                # print(f'ERROR | SERVER UDP | Unknown command: {command}')
                logging.warning(f"SERVER UDP | Unknown command: {command}")

    def start_listen(self, coordinator):
        self.udp_socket = self.create_and_bind_udp_listener()
        self.udp_listener(coordinator)
