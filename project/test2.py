import socket
import time
import socket
import threading
import pickle
import time

from structures.UDP_STR_RS import UDP_STR_RS
from structures.UDP_STR_INFO import UDP_STR_INFO

# BROADCAST NORS

def send(mess):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.sendto(mess, ('<broadcast>', 8888))
    print("message sent!")
    time.sleep(1)

# mess = 'RMRS'.encode()
# struc = UDP_STR_RS('88.23.35.52222', 2127, 'EOOO')
# struc_pickled = mess + pickle.dumps(struc)

mess = 'NORS'.encode()
struc = UDP_STR_INFO('82.23.35.532', 2127)
struc_pickled = mess + pickle.dumps(struc)

send(struc_pickled)

if (1, 2) in [(1, 2), (4, 5)]:
    print(1)