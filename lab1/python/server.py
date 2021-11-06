import socket
import sys


HOST = "127.0.0.1"
BUFSIZE = 100_000


if len(sys.argv) < 2:
    port = 8800
    print('Default port -> 8800')
elif len(sys.argv) > 2:
    print("Too many input data")
    sys.exit(0)
else:
    try:
        port = int(sys.argv[1])
    except Exception as e:
        print("Wrong input data!")
        sys.exit(0)


print(f"Will listen on {HOST}:{port}")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, port))
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
