#!/usr/bin/python3

import socket

scrap_tar='/tmp/scrap.tar'
scrap_zip='/tmp/scrap.zip'
#host = '192.168.1.104'
#host = socket.gethostname()
host = None
port = 444
READY = 3

with open(scrip_zip, 'r') as f:
    #Create socket object
    with  socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((host, port)) 
        #Receiving a maximum of 1024 bytes
        rcv = s.recv(1024)
        assert(rcv==READY)
        s.send(f.read())
