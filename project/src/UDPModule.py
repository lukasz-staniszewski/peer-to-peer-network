import threading
import socket
import logging

from project.src.Coordinator import remote_state_lock

UDP_PORT = 8888
BUFFER_SIZE = 1024
UDP_PERMITTED_MESS = ['GETS', 'NWRS', 'RMRS', 'NORS', 'SKIP']


class UDPModule:

    def __init__(self, addr,  udp_port=UDP_PORT, buffer_size=BUFFER_SIZE, permited_cmds=UDP_PERMITTED_MESS):
        self.UDP_PORT = udp_port
        self.BUFFER_SIZE = buffer_size
        self.address = addr
        self.UDP_PERMITTED_MESS = permited_cmds
        self.udp_socket = None

    def create_and_bind_udp_listener(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', self.UDP_PORT))
        return s

    def send_broadcast(self, mess):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.sendto(mess, ('<broadcast>', self.UDP_PORT))
        print("INFO | SERVER UDP | Broadcast sent!")
        logging.info("SERVER UDP | Broadcast sent!")

    def udp_listener(self, coordinator):
        print('INFO | SERVER UDP | UDP Listener is running')
        logging.info("SERVER UDP | UDP Listener is running")
        while True:
            m = self.udp_socket.recv(1024)
            command, payload = coordinator.deserialize_udp(m)
            # ignoring own broadcast
            if payload.ip_address == self.address:
                command = 'SKIP'
                print('INFO | SERVER UDP | Ignoring own broadcast!')
                logging.info("SERVER UDP | Ignoring own broadcast!")

            # send your list to node
            elif command == 'GETS':
                print('INFO | SERVER UDP | GOT GETS BROADCAST!')
                logging.info("SERVER UDP | GOT GETS BROADCAST!")
                add = payload.ip_address
                port = payload.port
                # sending my_files on specific address
                try:
                    coordinator.send_ndst(add, port)
                except Exception as e:
                    print(f'ERROR | SERVER UDP | Failed to send data -> {e}')
                    logging.warning(f"SERVER UDP | Failed to send data -> {e}")

            # node share new file
            elif command == 'NWRS':
                print('INFO | SERVER UDP | GOT NWRS BROADCAST!')
                logging.info(f"SERVER UDP | GOT NWRS BROADCAST!")
                add = payload.ip_address
                port = payload.port
                filename = payload.file_name
                with remote_state_lock:
                    coordinator.remote_state.add_to_others_files(filename, add, port)
                print(f'INFO | SERVER UDP | GOT NWRS BROADCAST | Uploaded: {filename}')
                logging.info(f"SERVER UDP | GOT NWRS BROADCAST | Uploaded: {filename}")

            #remove assigned node to specific file
            elif command == 'RMRS':
                add = payload.ip_address
                port = payload.port
                filename = payload.file_name
                with remote_state_lock:
                    coordinator.remote_state.remove_from_others_files(filename, add, port)
                print(f'INFO | SERVER UDP | GOT RMRS BROADCAST | Deleted: {filename}')
                logging.info(f"SERVER UDP | GOT RMRS BROADCAST | Deleted: {filename}")

            # node is now not sharing any files
            elif command == 'NORS':
                print(f'INFO | SERVER UDP | GOT NORS BROADCAST')
                logging.info(f"SERVER UDP | GOT NORS BROADCAST")
                add = payload.ip_address
                port = payload.port
                with remote_state_lock:
                    coordinator.remote_state.remove_node_from_others_files(add, port)

            if command not in UDP_PERMITTED_MESS:
                print(f'ERROR | SERVER UDP | Unknown command: {command}')
                logging.warning(f"SERVER UDP | Unknown command: {command}")

    def start_listen(self, coordinator):
        self.udp_socket = self.create_and_bind_udp_listener()
        self.udp_listener(coordinator)
