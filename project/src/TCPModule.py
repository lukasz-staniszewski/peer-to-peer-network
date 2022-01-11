import socket
import threading
from project.src.DataGenerator import DataGenerator
from project.src.DataDeserializer import DataDeserializer

LISTEN_PORT = 2115
BUFFER_SIZE = 1024


class TCPModule:
    def __init__(self, listen_port=LISTEN_PORT, buffer_size=BUFFER_SIZE):
        self.LISTEN_ADDRESS = '0.0.0.0'
        self.LISTEN_PORT = listen_port
        self.BUFFER_SIZE = buffer_size
        self.listen_socket = None

    def prepare_socket_listen(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.LISTEN_ADDRESS, self.LISTEN_PORT))
        listen_socket.listen(5)
        print("Server listening at port " + str(self.LISTEN_PORT))
        return listen_socket

    def prepare_socket_send(self, address, port):
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            send_socket.connect((address, port))
        except Exception as e:
            print(f'Can\'t establish a connection with {address, port}')

        return send_socket

    def send_data(self, socket_connection, data):
        try:
            socket_connection.sendall(data)
        except Exception as e:
            socket_connection.close()
            return e
        return 0

    def receive_data(self, socket_connection):
        data = b''
        while True:
            print(1)
            try:
                print(2)
                msg_data = socket_connection.recv(self.BUFFER_SIZE)
                print(3)
            except Exception as e:
                socket_connection.close()
                return e
            if not msg_data or msg_data[-1] == 4:
                data = data + msg_data
                break

            data += msg_data
        return data

    def listen_service(self, socket_connection, client_address, coordinator):
        data_decoder = DataDeserializer()
        print(
            "SERVER INFO | Connection from "
            + str(client_address[0])
            + ":"
            + str(client_address[1])
        )

        data = self.receive_data(socket_connection)

        if isinstance(data, Exception):
            print("SERVER ERROR | Cant read data! " + str(data))
            return

        command, payload = data_decoder.deserialize(data)

        print("SERVER INFO | Received command: " + command)

        if command == 'GETF':
            print('GETF command received')

            result = coordinator.send_file(socket_connection, payload)

            if result != 0:
                print("SERVER ERROR | Cant send back data! " + str(result))
                return
        elif command == 'NDST':
            print('NDST command received')
            coordinator.add_other_files(payload)
            print(coordinator.remote_state.others_files)
            print(f'State of node with address {(payload.ip_address, payload.port)} is: {payload.data}')
            socket_connection.close()
        else:
            print(f'UNKNOWN COMMAND: {command}')
            socket_connection.close()

        print(
            "SERVER INFO | Disconnection of "
            + str(client_address[0])
            + ":"
            + str(client_address[1])
        )

    def send_getf(self, send_socket, data):

        result = self.send_data(send_socket, data)

        if result != 0:
            print("ERROR | Cant send data! " + str(result))
            return

        data = self.receive_data(send_socket)

        if isinstance(data, Exception):
            print("SERVER ERROR | Cant read data! " + str(data))
            return

        send_socket.close()
        return data

    def send_ndst(self, send_socket, data):
        result = self.send_data(send_socket, data)

        if result != 0:
            print("ERROR | Cant send data! " + str(result))
            return

    def start_listen(self, coordinator):
        self.listen_socket = self.prepare_socket_listen()
        while True:
            client_socket, client_address = self.listen_socket.accept()
            threading.Thread(
                target=self.listen_service,
                args=(
                    client_socket,
                    client_address,
                    coordinator,
                ),
                daemon=True,
            ).start()


if __name__ == "__main__":
    tcp_module = TCPModule(LISTEN_PORT, BUFFER_SIZE)
    t_tcp = threading.Thread(target=tcp_module.start_listen)
    t_tcp.start()