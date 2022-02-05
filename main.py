import os.path
import threading
from project.src.TCPModule import TCPModule
from project.src.UDPModule import UDPModule
from project.src.Coordinator import Coordinator, local_state_lock, remote_state_lock
from project.File import File
import logging
import configparser


config = configparser.ConfigParser()
config.read("project/conf_log/conf.ini")

logging.basicConfig(
    level=logging.INFO,
    filename='project/conf_log/node.log',
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)


def print_interface():
    """
    Function prints user interface
    """
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


def main():
    config = configparser.ConfigParser()
    config.read("project/conf_log/conf.ini")

    udp_module = UDPModule(address=config['NET']['local_ip'], udp_port=int(config['UDP']['listen_port']),
                           buffer_size=int(config['UDP']['buffer_size']), permitted_cmds=config['UDP']['permitted_messages'])
    tcp_module = TCPModule(listen_address=config['TCP']['listen_address'], listen_port=int(config['TCP']['listen_port']),
                           buffer_size=int(config['TCP']['buffer_size']),
                           connection_close_simulation=int(config['TCP']['connection_close_simulation']),
                           additional_bytes_simulation=int(config['TCP']['additional_bytes_simulation']),
                           max_iterations=int(config['TCP']['max_iterations']))
    coordinator = Coordinator(address=config['NET']['local_ip'], udp_port=int(config['UDP']['listen_port']),
                              udp_module=udp_module, tcp_port=int(config['TCP']['listen_port']), tcp_module=tcp_module)

    t_udp = threading.Thread(target=udp_module.start_listen, args=[coordinator])
    t_udp.start()
    t_tcp = threading.Thread(target=tcp_module.start_listen, args=[coordinator])
    t_tcp.start()

    coordinator.send_nors()
    coordinator.get_others_files()

    while True:
        print_interface()
        try:
            usr_input = int(input('OPERATION: '))
        except ValueError:
            logging.warning("Wrong user input!")
            print("WRONG COMMAND!")
            continue

        # 1. ADD FILE [NWRS TEST]
        if usr_input == 1:
            file_name = str(input("FILE NAME: "))
            file_path = str(input("FILE PATH: "))
            if os.path.isfile(file_path):
                logging.info(f"Adding file to local resources. {file_name, file_path}")
                coordinator.add_local_file(File(filename=file_name, path=file_path))
            else:
                logging.warning("File with such path doesnt exists!")
                print("File with such path doesnt exists!")

        # 2. REMOVE FILE [RMRS TEST]
        elif usr_input == 2:
            file_name_remove = str(input("FILENAME TO REMOVE: "))
            coordinator.remove_local_file(file_name_remove)

        # 3. SEE YOUR LOCAL FILES
        elif usr_input == 3:
            with local_state_lock:
                logging.info(f"Your local files -> {coordinator.local_state.my_files}")
                print(coordinator.local_state.my_files)

        # 4. SEE OTHERS FILES
        elif usr_input == 4:
            with remote_state_lock:
                logging.info(f"See other files: {coordinator.remote_state.others_files}")
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
            coordinator.remove_all_local_files()
            os._exit(0) 

        # 8. GET OTHERS FILES
        elif usr_input == 8:
            coordinator.get_others_files()


if __name__ == '__main__':
    main()
