import socket
import time
import socket
import threading
import pickle
import time

from project.structures.UDP_STR_RS import UDP_STR_RS

# BROADCAST NWRS

def send(mess):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.sendto(mess, ('<broadcast>', 8888))
    print("message sent!")


mess = 'NWRS'.encode()
struc = UDP_STR_RS('82.23.35.532', 2127, 'a')
struc_pickled = mess + pickle.dumps(struc)
send(struc_pickled)


mess = 'NWRS'.encode()
struc = UDP_STR_RS('82.23.35.5321', 2127, 'b')
struc_pickled = mess + pickle.dumps(struc)
send(struc_pickled)

mess = 'NWRS'.encode()
struc = UDP_STR_RS('82.23.35.532', 2127, 'b')
struc_pickled = mess + pickle.dumps(struc)
send(struc_pickled)