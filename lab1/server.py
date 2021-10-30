import socket
import sys

HOST = '127.0.0.1' # Standard loopback interface address 
BUFSIZE = 512
# should check len(sys.argv), etc ...
port = int( sys.argv[1] )


print("Will listen on ", HOST, ":", port)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, port))
    i=1
    while True:
        data_address = s.recvfrom( BUFSIZE )
        data = data_address[0]
        address = data_address[1]
        print( "Message from Client:{}".format(data) )
        print( "Client IP Address:{}".format(address) )
        if not data:
            print("Error in datagram?")
            break
    # echo back data
        s.sendto(data, address )
        print('sending dgram #', i)
        i+=1