from riaps.run.comp import Component
import logging
import socket
import threading
import random

RTDS_IP = "192.168.1.104"
RTDS_PORT = 4575

VISUALIZATION_IP = "192.168.1.155"
VISUALIZATION_PORT = 4575




class RTDSDataProvider(Component):
    def __init__(self):
        super(RTDSDataProvider, self).__init__()
        print("Initializing Socket")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((RTDS_IP, RTDS_PORT))
        self.s.send('Start;'.encode())
        print("CONNECTED")

        msg = self.s.recv(64)
        print(msg)
        self.value = 85.0
        self.logger.info("Dataprovider initialized")

#        self.vis = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.vis.connect((VISUALIZATION_IP, VISUALIZATION_PORT))
        
    def on_clock(self):
        time = self.clock.recv_pyobj()
        msg = [100, 35, self.value, 45] 
        #msg = self.get_meter_values()
        self.logger.info("sending %s", str(msg))
        self.tempport.send_pyobj(msg)
        if self.value >= 96.0:
            self.value = random.uniform(81.0, 85.0)
            self.s.send('SetSlider "SL3" = {0:.2f};'.format(self.value/100).encode())

        #self.vis.send("R64".encode())
        
    def on_commandmsg(self):
        msg = self.commandmsg.recv_pyobj()
        self.value = msg * 100
        self.logger.info('SetSlider "SL3"= %f;', msg)
        self.s.send('SetSlider "SL3" = {};'.format(msg).encode())

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

    def parse_message(self, msg):
        msg_str = msg.decode()
        pg_str = msg_str.split(' ')[2]
        return float(pg_str)

