import os.path
import sys
import threading
import time
from src.TCPModule import TCPModule
from src.UDPModule import UDPModule
from src.Coordinator import Coordinator
from src.DataGenerator import DataGenerator
from File import File
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname("192.168.204.130")

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
    7. SHUTDOWN NODE & SEND BROADCAST
    8. GET OTHERS FILES
    """
    print(s)


if __name__ == '__main__':
    udp_module = UDPModule(addr=local_ip)
    tcp_module = TCPModule()
    coordinator = Coordinator(address, UDP_PORT, udp_module, TCP_PORT, tcp_module)

    t_udp = threading.Thread(target=udp_module.start_listen, args=[coordinator])
    t_udp.start()

    t_tcp = threading.Thread(target=tcp_module.start_listen, args=[coordinator])
    t_tcp.start()

    coordinator.get_others_files()

    data_gen = DataGenerator()
    while True:
        print_interface()
        try:
            usr_input = int(input('OPERATION: '))
        except ValueError:
            print("WRONG COMMAND!")
            continue
        # usr_input = int(input('OPERATION: '))
        # 1. ADD FILE [NWRS TEST]
        if usr_input == 1:
            file_name = str(input("FILENAME: "))
            file_path = str(input("FILEPATH: "))
            if os.path.isfile(file_path):
                coordinator.add_local_file(File(filename=file_name, path=file_path))
            else:
                print("File with such path doesnt exists!")
        # 2. REMOVE FILE [RMRS TEST]
        elif usr_input == 2:
            file_name_remove = str(input("FILENAME TO REMOVE: "))
            coordinator.remove_local_file(file_name_remove)
        # 3. SEE YOUR LOCAL FILES
        elif usr_input == 3:
            print(coordinator.local_state.my_files)
        # 4. SEE OTHERS FILES
        elif usr_input == 4:
            print(coordinator.remote_state.others_files)
        # 5. DOWNLOAD FILE [GETF TEST]
        elif usr_input == 5:
            file_name_download = str(input("FILENAME TO DOWNLOAD: "))
            coordinator.download_file(file_name_download)
        # 6. NODE INFO
        elif usr_input == 6:
            coordinator.print_info()
        # 7. SHUTDOWN NODE & SEND BROADCAST [NORS TEST]
        elif usr_input == 7:
            coordinator.send_nors()
            coordinator.local_state.remove_all_files()
            sys.exit(0)
        # 8. GET OTHERS FILES
        elif usr_input == 8:
            coordinator.get_others_files()
