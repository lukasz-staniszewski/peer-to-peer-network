import socket
import sys

N_MESSAGES = 6

def prepare_addr():
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

    return HOST, port

def create_socket_udp():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
def start_sending1(s, iterations, msg, addr):
    with s:
        for i in range(iterations):
            stream_data = msg
            try:
                print(f"Sending bytes: {len(stream_data)}")
                s.sendto(stream_data, (addr))
            except Exception as e:
                print(f"An error has occurred while sending data to server! Shutting down a client.", e)
                break

        print("Client finished.")

def start_sending2(s, msg, addr):
    with s:
        while True:
            stream_data = msg
            try:
                print(f"Sending bytes: {len(stream_data)}")
                s.sendto(stream_data, (addr))
            except Exception as e:
                print(f"An error has occurred while sending data to server! Shutting down a client.", e)
                break
            msg = msg * 2
        print("Client finished.")

if __name__=="__main__":
    msg = b'a'  # 1 byte message

    addr = prepare_addr()
    s = create_socket_udp()
    # start_sending1(s, N_MESSAGES, msg, addr)
    start_sending2(s, msg, addr)