import socket
import sys


if len(sys.argv) != 3:
    print(f"Usage is: {sys.argv[0]} <host> <port>")
    sys.exit(0)
else:
    try:
        port = int(sys.argv[2])
        HOST = sys.argv[1]
        hp = socket.gethostbyname(HOST)
    except Exception as e:
        print("Wrong input data!")
        sys.exit(0)

if hp != HOST:
    print(f"Unknown host {hp}, changing to 127.0.0.1")
    HOST = hp

message = b'a'  # 1 byte message
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for i in range(20):
        stream_data = message
        try:
            print(f"Sending bytes: {len(message)}")
            s.sendto(stream_data, (HOST, port))
        except Exception as e:
            print(f"An error has occurred while sending data to server! Shutting down a client.", e)
            break
        message = message * 2
print("Client finished.")
