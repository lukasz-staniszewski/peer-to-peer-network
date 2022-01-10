import threading
import socket


hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
address = local_ip
UDP_PORT = 8888
BUFFER_SIZE = 1024
UDP_PERMITTED_MESS = ['GETS', 'NWRS', 'RMRS', 'NORS']


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
        print("BROADCAST sent!")

    def udp_listener(self, coordinator):
        lock = threading.Lock()
        print('UDP Listener is running')
        while True:
            m = self.udp_socket.recv(1024)
            print('cos przyszlo na UDP')
            command, payload = coordinator.deserialize(m)
            # Ignorujemy BROADCASTA TO SAMYCH SIEBIE
            if payload.ip_address == address:
                command = 'SKIP'
            # Wyslij swoja liste plikow do danego wezla
            if command == 'GETS':
                add = payload.ip_address
                port = payload.port
                print(f'MAMY WYSLAC DO {payload.ip_address, payload.port}')
                # Teraz chcemy wyslac slownik my_files na dany adres
                try:
                    coordinator.send_ndst(add, port)
                except Exception as e:
                    print('Failed to send data')

            # Jakis wezel udostepnia nowy plik
            if command == 'NWRS':
                with lock:
                    add = payload.ip_address
                    port = payload.port
                    filename = payload.file_name
                    coordinator.remote_state.add_to_others_files(filename, add, port)
                print(f'UPLOADED other_files: {filename}')
            # Usun przypisany wezel do jakiegos pliku
            if command == 'RMRS':
                with lock:
                    add = payload.ip_address
                    port = payload.port
                    filename = payload.file_name
                    coordinator.remote_state.remove_from_others_files(filename, add, port)
                print(f'Deleted from other_files: {filename}')
            # Dany wezel nie udostepnia juz zadnych plikow
            if command == 'NORS':
                with lock:
                    add = payload.ip_address
                    port = payload.port
                    coordinator.remote_state.remove_node_from_others_files(add, port)
            if command not in UDP_PERMITTED_MESS:
                print(f'Unknown command: {command}')

    def start_listen(self, coordinator):
        self.udp_socket = self.create_and_bind_udp_listener()
        self.udp_listener(coordinator)
