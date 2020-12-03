#!/usr/bin/python3

import socket

scrap_tar='/tmp/scrap.tar'
scrap_zip='/tmp/scrap.zip'

host = socket.gethostname() #Host is the server IP
port = 444 #Port to listen on
READY=3

with open(scap_zip, 'w') as f:
    #Creating the socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
        #Binding to socket
        ##Host will be replaced/substitued with IP, if changed and not running on host
        ss.bind((host, port)) 
        #Starting TCP listener
        ss.listen(3)
        while True:
            #Starting the connection 
            clientsocket,address = ss.accept()
            print("received connection from " % str(address))
            ss.send(READY)
            f.write(ss.read())
