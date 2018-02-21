import socket
import csv
from datetime import datetime

NORMAL_FILE = "../Data/cs01_no_ls.csv"

def parse_files():

        normalFile = open(NORMAL_FILE, 'r') 

        normalReader = csv.reader(normalFile)

        normalReadings = list()

        normalTimes = list()

        for row in normalReader:
            normalReadings.append(float(row[1].strip()))
        
            #Get all the dates and times and then display them
            normalTimes.append(datetime.strptime(row[0].strip(), '%m/%d/%Y %X.%f'))
        


        normalFile.close()

        return normalReadings, normalTimes

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    normalReadings, normalTimes = parse_files()

    s.bind(("127.0.0.1", 4575))

    s.listen(1)
    sock, addr = s.accept()


    with open(NORMAL_FILE, 'r') as f:

        for i in range(len(normalReadings)):
            recv_str = sock.recv(64)
            sock.send(f.readline().replace(',', ''))

    sock.close()            

main()
