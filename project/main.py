import socket
import threading
import pickle
import time

from structures.UDP_STR_RS import UDP_STR_RS
from structures.UDP_STR_INFO import UDP_STR_INFO
from structures.TCP_STR_CONT import TCP_STR_CONT
from structures.TCP_STR_INFO import TCP_STR_INFO

UDP_PERMITTED_MESS = ['GETS', 'NWRS', 'RMRS', 'NORS']
TCP_PERMITTED_MESS = ['GETF', 'FILE', 'DECF', 'NDST', 'EMPS']

address = '192.168.100.6'
udp_port = 8888
tcp_port = 2115


def prepare_my_files(address, udp_port, tcp_port):
    return {
        'address': address,
        'udp_port': udp_port,
        'tcp_port': tcp_port,
        'files': []
    }


def send_broadcast(mess):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.sendto(mess, ('<broadcast>', udp_port))
    print("BROADCAST sent!")


def add_local_file(filename, my_files):
    files = my_files['files']
    if filename in files:
        return False
    files.append(filename)
    my_files['files'] = files
    # Wyslij BROADCAST, ze dodalem plik --> 'NWRS' + UDP_STR_RS
    port = tcp_port

    struc = UDP_STR_RS(address, port, filename)
    struc_pickled = pickle.dumps(struc)

    command = 'NWRS'.encode()
    print(f'SENDING NWRS, filename: {filename}')
    send_broadcast(command+struc_pickled)
    return True


def remove_local_file(filename, my_files):
    files = my_files['files']
    if filename not in files:
        return False
    files.remove(filename)
    my_files['files'] = files
    # Wyslij BROADCAST, ze dodalem plik --> 'NWRS' + UDP_STR_RS
    address = my_files[0]
    port = my_files[1]

    struc = UDP_STR_RS(address, filename, port)
    struc_pickled = pickle.dumps(struc)

    command = 'RMRS'.encode()
    print(f'SENDING RMRS, filename: {filename}')
    send_broadcast(command + struc_pickled)


def create_and_bind_udp_listener(udp_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', udp_port))
    return s


def create_and_bind_tcp_listener(tcp_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.100.6', tcp_port))
    return s


def add_to_others_files(others_files, filename, address, port):
    if filename in others_files.keys():
        curr_files = others_files[filename]
        if (address, port) not in others_files[filename]:
            curr_files.append((address, port))
        others_files[filename] = curr_files
    else:
        others_files[filename] = [(address, port)]


def remove_from_others_files(others_files, filename, address, port):
    if filename in others_files.keys():
        if len(others_files[filename]) == 1:
            others_files.pop(filename)
            return True
        else:
            curr_files = others_files[filename]
            curr_files.remove((address, port))
            others_files[filename] = curr_files
            return True
    return False


def remove_node_from_others_files(others_files, address, port):
    keys_to_delete = []
    for key, val in others_files.items():
        print(val)
        print(f'want to remove {(address, port)}')
        if (address, port) in val:
            if len(val) == 1:
                keys_to_delete.append(key)
            else:
                val.remove((address, port))
            print(f'removing {(address, port)}')

    for key in keys_to_delete:
        others_files.pop(key)


def udp_listener(others_files, s):
    lock = threading.Lock()
    print('UDP Listener is running')
    while True:
        m = s.recv(1024)
        print('cos przyszlo na UDP')
        command = m[0:4].decode()
        payload = m[4:]
        payload = pickle.loads(payload)
        command = command.upper()
        # Ignorujemy BROADCASTA TO SAMYCH SIEBIE
        if payload.ip_address == address:
            command = 'SKIP'
        # Wyslij swoja liste plikow do danego wezla
        if command == 'GETS':
            add = payload.ip_address
            port = payload.port
            print(f'MAMY WYSLAC DO {payload.ip_address, payload.port}')
            # Teraz chcemy wyslac slownik my_files na dany adres
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((add, port))
            except Exception as e:
                print(f'Can\'t establish a connection with {add, port}')

            try:
                mess = 'NDST'.encode()
                struc = TCP_STR_CONT(add, port, None, ['elo.txt', 'abc.asm', 'google.jpg'])
                struc_pickled = mess + pickle.dumps(struc)
                s.sendall(struc_pickled)
            except Exception as e:
                print('Failed to send data')

        # Jakis wezel udostepnia nowy plik
        if command == 'NWRS':
            with lock:
                add = payload.ip_address
                port = payload.port
                filename = payload.file_name
                add_to_others_files(others_files, filename, add, port)
            print(f'UPLOADED other_files: {filename}')
        # Usun przypisany wezel do jakiegos pliku
        if command == 'RMRS':
            with lock:
                add = payload.ip_address
                port = payload.port
                filename = payload.file_name
                remove_from_others_files(others_files, filename, add, port)
            print(f'Deleted from other_files: {filename}')
        # Dany wezel nie udostepnia juz zadnych plikow
        if command == 'NORS':
            with lock:
                add = payload.ip_address
                port = payload.port
                remove_node_from_others_files(others_files, add, port)
        if command not in UDP_PERMITTED_MESS:
            print(f'Unknown command: {command}')


def tcp_listener(other_files, my_files, s):
    lock = threading.Lock()
    s.listen(5)
    print('TCP Listener is running')
    while True:
        conn, addr = s.accept()
        print(conn)
        m = conn.recv(1024)
        command = m[0:4].decode()
        payload = m[4:]
        payload = pickle.loads(payload)
        command = command.upper()
        if command == 'NDST':
            print(f'State of node with address {(payload.ip_address, payload.port)} is: {payload.data}')
            # TODO: Aktualizacja other_files
        else:
            print(f'UNKNOWN COMMAND: {command}')


def get_others_files(address, tcp_port):
    struc = UDP_STR_INFO(address, tcp_port)
    struc_pickled = pickle.dumps(struc)
    command = 'GETS'.encode()
    send_broadcast(command+struc_pickled)


if __name__ == '__main__':
    # address: ...   port: ...   files: ... (files na poczatku jest puste)
    my_files = prepare_my_files(address, udp_port, tcp_port)

    udp_listener_socket = create_and_bind_udp_listener(udp_port)

    tcp_listener_socket = create_and_bind_tcp_listener(tcp_port)

    others_files = {}

    t_udp = threading.Thread(target=udp_listener, args=[others_files, udp_listener_socket])
    t_udp.start()

    t_tcp = threading.Thread(target=tcp_listener, args=[others_files, my_files, tcp_listener_socket])
    t_tcp.start()

    add_local_file('helloworlds.asm', my_files)

    # TODO: Ta funkcja buguje dzialanie broadcastu np NWRS
    get_others_files(address, tcp_port)

    while True:
        print(others_files)
        time.sleep(2)
