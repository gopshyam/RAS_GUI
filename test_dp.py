import socket
import threading
import time

RTDS_IP = "192.168.1.102"
RTDS_PORT = 4575


class RTDSConnection():
    def __init__(self):
        self.s = None
        self.pdc = None
        self.dframes = None
        self.lock = threading.Lock()
        self.connect_RTDS()

    def connect_RTDS(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((RTDS_IP, RTDS_PORT))
        time.sleep(3)
        self.s.send('Start;'.encode())

        msg = self.s.recv(64)
        print(msg)
        return True

    def parse_message(self, msg):
        msg_str = msg.decode()
        pg_str = msg_str.split(' ')[2]
        return float(pg_str)

    def get_meter_values(self):
        tempPG = list()
        for i in range(1,5):
            string1 = 'temp_float = MeterCapture("PG{}");'.format(i).encode()
            string2 = 'sprintf(temp_string, "PG{} = %f END", temp_float);'.format(i).encode()
            string3 = "ListenOnPortHandshake(temp_string);".encode()


            self.s.send(string1)
            self.s.send(string2)
            self.s.send(string3)

            msg = ''.encode()

            while("PG" not in msg.decode()):
                msg = self.s.recv(64)
                print(msg)
            pg_value = self.parse_message(msg)
            tempPG.append(pg_value)

        return tempPG

    def send_command(self, cmd):
        self.s.send(cmd.encode())



rc = RTDSConnection()
rc.connect_RTDS()
time.sleep(3)
print(rc.get_meter_values())
