import socket
import sys

HOST = "127.0.0.1"

if len(sys.argv) < 2:
    port = 8800
    print("Setting default port: 8800")
elif len(sys.argv) > 2:
    print("Wrong parameters")
    sys.exit(0)
else:
    try:
        port = int(sys.argv[1])
    except Exception as e:
        print("Wrong Input Data!")
        sys.exit(0)

message = b'a'  # 1 byte message
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for i in range(13):
        stream_data = message
        try:
            s.sendto(stream_data, (HOST, port))
            data = s.recv(len(message))
        except Exception as e:
            print("Fatal error has occurred while receiving data from a server. Server might not be running.\n"
                  "Shutting down a client.")
            sys.exit(0)
        message = message * 2
        print(f"Received data={repr(data)} size={len(message)}")
print("Client finished.")
