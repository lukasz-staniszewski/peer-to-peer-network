import socket
import sys

BUFSIZE = 100
HOST = '0.0.0.0'

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

def create_socket_udp():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def bind_socket(s, port):
    try:
        s.bind((HOST, port))
    except Exception as e:
        print("Error while binding")
        sys.exit(1)

def get_server_port_info(s):
    port = 0
    try:
        port = s.getsockname()
    except Exception as e:
        print("Error while getting socket name")
        sys.exit(1)

    print(f"Will listen on {HOST}:{port}")


def run_server_reading(s):
    with s:
        while True:
            try:
                data_address = s.recvfrom(BUFSIZE)
            except Exception as e:
                print("An error has occurred with the current client (too big datagram has been sent)", e)
                break
            data = data_address[0]
            address = data_address[1]
            print(f"Bytes from Client: {len(data)}")
            print( "Message from Client:{}".format(data) ) 
            print(f"Client IP Address: {address}")
            if not data:
                print("Error in datagram")
                break

if __name__=="__main__":
    port = prepare_socket_address()
    s = create_socket_udp()
    bind_socket(s, port)
    get_server_port_info(s)
    run_server_reading(s)