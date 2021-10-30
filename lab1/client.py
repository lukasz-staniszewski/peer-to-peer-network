import socket
import sys
import io

HOST = '127.0.0.1' # The server's hostname or IP address
# should check len(sys.argv), etc ...
port = int( sys.argv[1] )

size = 80
binary_stream = ''

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # binary_stream.write("Hello, world!\n".encode('ascii'))
    # binary_stream.seek(0)
    # stream_data = binary_stream.read()
    stream_data = 'abcdef\n'.encode('ascii')
    for i in range(10):
        s.sendto( stream_data, (HOST, port) )
        data = s.recv( size )
        print('Received data=', repr(data), " size= ", size )
print('Client finished.')
