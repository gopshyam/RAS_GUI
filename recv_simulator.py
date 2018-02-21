import socket

def parse_message(msg_bstr):
    msg_str = msg_bstr.decode()
    pmsg_str = msg_str.split(' ')[2]
    pmsg_float = float(pmsg_str)
    return pmsg_float

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 4575))

print "Connection Established"



recv_string = "test"
while recv_string:
    s.send("Data plz")
    recv_string = s.recv(1024)
    print recv_string
    print parse_message(recv_string)



