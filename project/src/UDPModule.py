import socket
import logging
import ast
from project.src.Coordinator import remote_state_lock


class UDPModule:
    """
    Represents UDP module.
    """
    def __init__(self, address,  udp_port, buffer_size, permitted_cmds):
        """
        UDPModule constructor.

        :param address: address on which socket listens for broadcasts
        :param udp_port: port on which socket listens for broadcasts
        :param buffer_size: size of buffer for receiving data
        :param permitted_cmds: possible udp commands in messages
        """
        self.port = udp_port
        self.buffer_size = buffer_size
        self.address = address
        self.permitted_messages = ast.literal_eval(permitted_cmds)
        self.udp_socket = None

    def create_and_bind_udp_listener(self):
        """
        Creates udp socket and binds it.
        :return: socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))
        return sock

    def send_broadcast(self, message):
        """
        Performs send of single broadcast.

        :param message: message to send
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server.sendto(message, ('<broadcast>', self.port))
        logging.info("SERVER UDP | Broadcast sent!")

    def udp_listener(self, coordinator):
        """
        Performs udp listening logic.

        :param coordinator: coordinator object
        """
        logging.info("SERVER UDP | UDP Listener is running")
        while True:
            message = self.udp_socket.recv(self.buffer_size)
            command, payload = coordinator.deserialize_udp(message)
            # ignoring own broadcast
            if payload.ip_address == self.address:
                command = 'SKIP'
                logging.info("SERVER UDP | Ignoring own broadcast!")

            # send your list to node
            elif command == 'GETS':
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
                logging.info(f"SERVER UDP | GOT NORS BROADCAST")
                address = payload.ip_address
                port = payload.port
                with remote_state_lock:
                    coordinator.remote_state.remove_node_from_others_files(address, port)

            if command not in self.permitted_messages:
                logging.warning(f"SERVER UDP | Unknown command: {command}")

    def start_listen(self, coordinator):
        """
        Performs listening.

        :param coordinator: coordinator of object
        """
        self.udp_socket = self.create_and_bind_udp_listener()
        self.udp_listener(coordinator)
