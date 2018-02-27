import socket
import time

RTDS_IP = "192.168.1.102"
RTDS_PORT = 4575

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RTDS_IP, RTDS_PORT))

s.send('Start;'.encode())

msg = s.recv(64)
print(msg)


time.sleep(2)

msg = s.recv(64)
print(msg)
