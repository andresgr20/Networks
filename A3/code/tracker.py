#!/usr/bin/env python3

import socket,sys,_thread, random, threading,os, pickle
from files import Files
import struct

# port for the server
serverPort = 20238
peer = 0
# Obtains the lock for the printing on the screen
mutex = _thread.allocate_lock()

# Array of the files to keep track of
files = []

# Alive fellas 
peers = []

# create the unique number for each peer
def unique_assign():
    global peer
    peer =+ 1
    return str(peer)

# Pulls the current status of the chunks 
def pull():
    return

def create_track(file_name, size,chunks,IP, port):
    files.append(Files(size,chunks,file_name,IP,port))
    peers.append([IP,port])
    

def peer_connect(p, fno):
    msg_connect = "PEER "+ str(p) +" CONNECT: OFFERS " + str(fno) 
    msg_file_info = str(p) + "    " + files[0].get_name() + " " + str(files[0].get_chunk_total())
    print(msg_connect)
    print(msg_file_info)

def chunk_total(file_name):
    return

def print_msg(code,data):
    global mutex
    mutex.acquire()
    if(code == 1):
        peer_connect(data)
    elif (code == 2):
        peer_downloaded(data)
    else:
        peer_disconnect(data)
    mutex.release()
    
def peer_downloaded():
    chunk = 1
    file_name = "hi"
    msg = "PEER" + peer + "ACQUIRED: CHUNK " + chunk + "/" + chunk_total(file_name) + " " + file_name
    print(msg)

def find_files_owned(p):
    f = []
    for i in files:
        if(p in i.get_owners()):
            f.append(i.get_name())
    return f

def remove_owner(p):
    for i in files:
        if(p in i.get_owners()):
            i.remove_owner(p)

def peer_disconnect(p):
    owned = find_files_owned(p)
    msg = "PEER " + str(p) + " DISCONNECT: RECEIVED " + str(len(owned))
    print(msg)
    for i in owned:
        print(str(p) + "    " + i)

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# Need to fix the creation of the initial array of data
def bootup_tracker():
    port = 38438
    # picks a port and write it to the port.txt file
    f= open("port.txt","w+")
    f.write(str(port))
    f.close()    
    data = []
    peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peerSocket.bind(('localhost', port))
    peerSocket.listen(10)
    print('Waiting for connections + Info from the peer')
    connectionSocket, addr = peerSocket.accept()
    connectionSocket.send(unique_assign().encode())
    if(peer not in peers and not peers):
        new_arrival(connectionSocket)
    peers.append(peer)
    data.append(peer)
    # The array is forming weird need to fix, everything is merging into one big thing
    while True:
        d = connectionSocket.recv(1024).decode()
        if not d: break
        data.append(d)
    print(data)
    files.append(Files(63900, 126,'Screen Shot 2019-11-26 at 1.22.04 PM.png','localhost',38438,peer))
    # peer_connect(peer,1)

    # connectionSocket, addr = peerSocket.accept()
    
    # msg = connectionSocket.recv(1024).decode()

    # sends the peer number to the user
    # while True:
    #     data.append(socket.recv(1024).decode())
    #     if not data: 
    #         create_track()
    #         data = []
    #         break 
    

def new_arrival(s):
    msg = "200"
    s.send(msg.encode())

if __name__ == '__main__':
    bootup_tracker()
    # print_msg(2)