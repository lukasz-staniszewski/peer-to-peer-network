import socket
import sys


def prepare_socket_address():
    if len(sys.argv) != 1 and len(sys.argv) != 2:
        print("Usage is: nothing or <port>")
        sys.exit(0)
    if len(sys.argv) == 2:
        try:
            if int(sys.argv[1])>-1 and int(sys.argv[1])<65536:
                port = int(sys.argv[1])
            else:
                port = 0
        except Exception as e:
            print("Invalid port!")
            sys.exit(1)
    else:
        print("Port not specified. Using random!")
        port = 0

    return port

def listen(port):
    server_socket = socket.socket()
    server_socket.bind((SERVER_HOST, port))
    server_socket.listen(5)
    print("listening")
    return server_socket


def receive_data(server_socket):
    while True:
        client_socket = server_socket.accept()[0]
        print("connected")
        data = client_socket.recv(BUFFER_SIZE).decode()
        print(data)


if __name__ == '__main__':
    BUFFER_SIZE = 1024
    port = prepare_socket_address()
    print(port)
    SERVER_HOST = "0.0.0.0"
    server_socket = listen(port)
    receive_data(server_socket)