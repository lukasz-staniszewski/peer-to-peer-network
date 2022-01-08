import pickle
import time
import socket

from structures.TCP_STR_CONT import TCP_STR_CONT
from structures.UDP_STR_RS import UDP_STR_RS

address = '192.168.1.15'
port = 2115

# TCP - wysylamy stan

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
mess = 'NDST'.encode()
struc = TCP_STR_CONT(address, port, None, ['elo.txt', 'siema.asm', 'balbinka.jpg'])
struc_pickled = mess + pickle.dumps(struc) + '\4'.encode()
s.sendall(struc_pickled)