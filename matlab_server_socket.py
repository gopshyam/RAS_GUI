from matlab_interface import MatlabInterface
import socket
import threading


def handle_connection(clientsocket):
	while(True):
		args = clientsocket.recv(32)
		print args


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('127.0.0.1', '4567'))
serversocket.listen(5)

m_inf = MatlabInterface()

while True:
	(clientsocket, address) = serversocket.accept()
	
