import socket
import sys
import time

BUFFER_SIZE = 1024

data = "GETF siema.txt" + "\0"

HOST = "127.0.0.1"
PORT = 2115


def setup_connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"CLIENT INFO | Connecting to {host}:{port}!")
    try:
        s.connect((host, port))
    except Exception as e:
        print(
            "CLIENT ERROR | Cant connect to host: "
            + str(host)
            + ":"
            + str(port)
            + "! "
            + str(e)
        )
        sys.exit(1)
    print("CLIENT INFO | Connected.")
    return s


def receive_data(socket):
    data = ""
    while True:
        try:
            msg_data = socket.recv(BUFFER_SIZE)

        except Exception as e:

            print("SERVER ERROR | Cant read data! " + str(e))

            socket.close()
            return

        if not msg_data:
            break
    data = data + msg_data.decode()

    return data

def send_data(s, data):

    print("CLIENT INFO | Sending data started.")
    try:
        s.sendall(data.encode())
        print("CLIENT INFO | Sending data finished.")

    except Exception as e:
        print("CLIENT ERROR | Cant send data! " + str(e))
        sys.exit(1)

    data = ""
    while True:
        try:
            msg_data = s.recv(BUFFER_SIZE)

        except Exception as e:

            print("SERVER ERROR | Cant read data! " + str(e))

            socket.close()
            return

        if not msg_data:
            break
        data = data + msg_data.decode()

    print("Received data: " + data)


if __name__ == "__main__":
    print("CLIENT INFO | Client process started.")
    soc = setup_connection(HOST, PORT)
    send_data(soc, data)
    print("CLIENT INFO | Client process finished.")
    print(sys.getsizeof(data))
