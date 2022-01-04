import socket
import sys
import threading

BUFFER_SIZE = 1024
LISTEN_ADDRESS = "0.0.0.0"
LISTEN_PORT = 2115
console_lock = threading.Lock()

send_data = "siemanderodsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss" \
       "dssssssssssssssssssssssssssssssssssssssssssssssssssssfdsfffffffffffffffffffffffffffffffffffff" \
       "fdssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss" \
       "fdsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssa" \
       "fdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd" \
       "dssssssssssssssssssssssssssaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
       "sddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddffffffffffffffffffffffffffffffff" \
       "assssssssssssssssssssssssssssssssssssssssaaaaaasaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
       "fddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd" \
       "fdsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasddddddddddaaaaaaaaaaaaaaaaaaaaaaasssssssssssssss" \
       "dssssssssssssssssssssssssssssssssssssssssssssxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxd" + "\0"


def service(socket_connection, client_address):

    print(
        "SERVER INFO | Connection from "
        + str(client_address[0])
        + ":"
        + str(client_address[1])
    )

    try:
        data = socket_connection.recv(BUFFER_SIZE)
    except Exception as e:
        print("SERVER ERROR | Cant read data! " + str(e))
        socket_connection.close()
        return

    data = data.decode()

    print("SERVER INFO | Received: " + data)

    data = send_data

    try:
        socket_connection.sendall(data.encode())
        print("Send data :" + data)
    except Exception as e:
        print("SERVER ERROR | Cant send back data! " + str(e))
        socket_connection.close()
        return

    print(
        "SERVER INFO | Disconnection of "
        + str(client_address[0])
        + ":"
        + str(client_address[1])
    )

    socket_connection.close()


def prepare_socket_listen(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((LISTEN_ADDRESS, port))
    server_socket.listen(5)
    print("Server listening at port " + str(port))
    return server_socket


def start_receiving(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(
            target=service,
            args=(
                client_socket,
                client_address,
            ),
            daemon=True,
        ).start()


if __name__ == "__main__":
    server_socket = prepare_socket_listen(LISTEN_PORT)
    start_receiving(server_socket)
    server_socket.close()

