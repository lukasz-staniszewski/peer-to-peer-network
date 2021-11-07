import socket
import sys

BUFSIZE = 100
HOST = '0.0.0.0'

if len(sys.argv) != 1 and len(sys.argv) != 2:
    print("Usage is: nothing or <port>")
    sys.exit(0)
if len(sys.argv) == 2:
    try:
        port = int(sys.argv[1])
    except Exception as e:
        print("Invalid port!")
        sys.exit(0)
else:
    print("Port not specified. Using random!")
    port = 0


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, port))
    port = s.getsockname()
    print(f"Will listen on {HOST}:{port}")
    while True:
        try:
            data_address = s.recvfrom(BUFSIZE)
        except Exception as e:
            print("An error has occurred with the current client (too big datagram has been sent)")
            break
        data = data_address[0]
        address = data_address[1]
        print(f"Bytes from Client: {len(data)}")
        print(f"Client IP Address: {address}")
        if not data:
            print("Error in datagram")
            break
