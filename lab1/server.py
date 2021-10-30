import socket
import sys


HOST = "127.0.0.1"
BUFSIZE = 512


if len(sys.argv) < 2:
    port = 8800
    print('Default port -> 8800')
elif len(sys.argv) > 2:
    print("Too many input data")
    sys.exit(0)
else:
    try:
        port = int( sys.argv[1] )
    except Exception as e:
        print("Wrong input data!")
        sys.exit(0)


print(f"Will listen on {HOST}:{port}")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, port))
    i = 1
    while True:
        try:
            data_address = s.recvfrom(BUFSIZE)
        except Exception as e:
            print("An error has occurred with the current client (too big datagram)")
            #  ???
            s.sendto(bytearray(0), address)
            break
        data = data_address[0]
        address = data_address[1]
        print(f"Message from Client: {data}")
        print(f"Client IP Address: {address}")
        if not data:
            print("Error in datagram?")
            break
        # echo back data
        try:
            s.sendto(data, address)
            print(f"sending dgram #{i}")
        except Exception as e:
            print("An error has occurred while sending data to a client")
            break
        i += 1
