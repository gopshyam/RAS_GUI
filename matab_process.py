from matlab_interface import MatlabInterface
import socket

m_inf = MatlabInterface()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 3400))
s.listen(5)
print("LISTENING")

while True:
	(clientsocket, address) = s.accept()
	msg = clientsocket.recv(200)
	PGstr = msg.decode().split(" ")
	tempPG = [float(x) for x in PGstr]
	res = m_inf.compute_result(tempPG)
	print(res)
	r = [str(x[0]) for x in res]
	clientsocket.send(" ".join(r).encode())

