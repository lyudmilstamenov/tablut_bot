

import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.189.129', 5800))
print('connected')
s.sendall('WHITE azz'.encode())
print('connected')
data = s.recv(100)
print('received')
print(data)

while True:
    data = s.recv(1024)
    print(data)

    s.sendall('WHITE azz'.encode())
    print('move')

s.close()