import socket
import sys

def prepare_addr():
    if len(sys.argv) != 3:
        print(f"Usage is: {sys.argv[0]} <host> <port>")
        sys.exit(1)
    else:
        try:
            if int(sys.argv[2])>-1 and int(sys.argv[2])<65536:
                port = int(sys.argv[2])
            else:
                print("Invalid port, should be in range 0-65535")
                sys.exit(1)
            HOST = sys.argv[1]
            hp = socket.gethostbyname(HOST)
        except Exception as e:
            print("Wrong input data!")
            sys.exit(1)

    if hp != HOST:
        print(f"Unknown host {hp}, changing to 127.0.0.1")
        HOST = hp

    return HOST, port

def setup_connection(host, port):
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    return s


def send_data(s, data):
    print("[+] sending.")
    s.send(data.encode())
    print("[+] data sent.")


if __name__ == "__main__":
    data = "abcdefgh"
    HOST, PORT = prepare_addr()
    soc = setup_connection(HOST, PORT)
    send_data(soc, data)