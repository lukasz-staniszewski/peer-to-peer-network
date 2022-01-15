import threading
import socket


hostname = socket.gethostname()
local_ip = socket.gethostbyname("192.168.204.128")
address = local_ip
# address = "192.168.204.130"
UDP_PORT = 8888
BUFFER_SIZE = 1024
UDP_PERMITTED_MESS = ['GETS', 'NWRS', 'RMRS', 'NORS', 'SKIP']


class UDPModule:

    def __init__(self, addr=address,  udp_port=UDP_PORT, buffer_size=BUFFER_SIZE, permited_cmds=UDP_PERMITTED_MESS):
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
        print("INFO | SERVER UDP | BROADCAST sent!")

    def udp_listener(self, coordinator):
        lock = threading.Lock()
        print('INFO | SERVER UDP | UDP Listener is running')
        while True:
            m = self.udp_socket.recv(1024)
            command, payload = coordinator.deserialize(m)
            # ignoring own broadcast
            if payload.ip_address == address:
                command = 'SKIP'
                print('INFO | SERVER UDP | Ignoring own broadcast!')
            # send your list to node
            elif command == 'GETS':
                add = payload.ip_address
                port = payload.port
                # sending my_files on specific address
                try:
                    coordinator.send_ndst(add, port)
                except Exception as e:
                    print('ERROR | SERVER UDP | Failed to send data')
            # node share new file
            elif command == 'NWRS':
                add = payload.ip_address
                port = payload.port
                filename = payload.file_name
                with lock:
                    coordinator.remote_state.add_to_others_files(filename, add, port)
                print(f'INFO | SERVER UDP | UPLOADED other_files: {filename}')
            # remove assigned node to specific file
            elif command == 'RMRS':
                add = payload.ip_address
                port = payload.port
                filename = payload.file_name
                with lock:
                    coordinator.remote_state.remove_from_others_files(filename, add, port)
                print(f'INFO | SERVER UDP | Deleted from other_files: {filename}')
            # node is now not sharing any files
            elif command == 'NORS':
                add = payload.ip_address
                port = payload.port
                with lock:
                    coordinator.remote_state.remove_node_from_others_files(add, port)
            if command not in UDP_PERMITTED_MESS:
                print(f'ERROR | SERVER UDP | Unknown command: {command}')

    def start_listen(self, coordinator):
        self.udp_socket = self.create_and_bind_udp_listener()
        self.udp_listener(coordinator)
