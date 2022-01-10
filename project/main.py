import threading
import time
from src.TCPModule import TCPModule
from src.UDPModule import UDPModule
from src.Coordinator import Coordinator
from src.DataGenerator import DataGenerator
from File import File
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

address = local_ip
UDP_PORT = 8888
TCP_PORT = 2115
BUFFER_SIZE = 1024


def print_interface():
    s = """
    1. ADD FILE
    2. REMOVE FILE
    3. SEE YOUR FILES
    4. SEE OTHERS FILES
    5. DOWNLOAD FILE
    6. NODE INFO
    """
    print(s)


if __name__ == '__main__':
    # address: ...   port: ...   files: ... (files na poczatku jest puste)
    udp_module = UDPModule()
    tcp_module = TCPModule()

    coordinator = Coordinator(address, UDP_PORT, udp_module, TCP_PORT, tcp_module)

    t_udp = threading.Thread(target=udp_module.start_listen, args=[coordinator])
    t_udp.start()

    t_tcp = threading.Thread(target=tcp_module.start_listen, args=[coordinator])
    t_tcp.start()

    # coordinator.add_local_file(File('helloworlds.txt', "balbinka"))

    coordinator.get_others_files()

    data_gen = DataGenerator()
    while True:
        print_interface()
        usr_input = int(input('OPERATION: '))
        # 1. ADD FILE
        if usr_input == 1:
            file_name = str(input("FILENAME: "))
            coordinator.add_local_file(File(file_name, data_gen.generate_data(10)))
        # 2. REMOVE FILE
        elif usr_input == 2:
            file_name_remove = str(input("FILENAME TO REMOVE: "))
            coordinator.remove_local_file(file_name_remove)
        # 3. SEE YOUR LOCAL FILES
        elif usr_input == 3:
            print(coordinator.local_state.my_files)
        # 4. SEE OTHERS FILES
        elif usr_input == 4:
            print(coordinator.remote_state.others_files)
        # 5. DOWNLOAD FILE
        elif usr_input == 5:
            file_name_download = str(input("FILENAME TO DOWNLOAD: "))
            coordinator.download_file(file_name_download)
        # 6. NODE INFO
        elif usr_input == 6:
            coordinator.print_info()
