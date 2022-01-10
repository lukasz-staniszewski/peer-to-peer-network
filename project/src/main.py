import threading
import time
from TCPModule import TCPModule
from UDPModule import UDPModule
from Coordinator import Coordinator


# address = '192.168.100.6'
address = '192.168.0.81'
UDP_PORT = 8888
TCP_PORT = 2115
BUFFER_SIZE = 1024

if __name__ == '__main__':
    # address: ...   port: ...   files: ... (files na poczatku jest puste)
    # my_files = prepare_my_files(address, UDP_PORT, TCP_PORT)
    coordinator = Coordinator(address, UDP_PORT, TCP_PORT)

    udp_module = UDPModule()
    tcp_module = TCPModule()

    t_udp = threading.Thread(target=udp_module.start_listen, args=[coordinator])
    t_udp.start()

    t_tcp = threading.Thread(target=tcp_module.start_listen)
    t_tcp.start()

    coordinator.add_local_file('helloworlds.asm')

    coordinator.get_others_files()

    while True:
        print(coordinator.remote_state.others_files)
        time.sleep(2)
