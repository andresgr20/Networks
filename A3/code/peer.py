#!/usr/bin/env python3

import socket,sys,_thread, random, threading,os


# Max number of peers
N = 8
CHUNKY_SIZE = 512
chunks = []
files = []
size = 0

#Peer ID
peer = 0

 # Need to add threads to this
# Obtains the chunks and the size of the file
def process_file():
    global size
    file_list =  os.listdir("./Shared")
    files.append(file_list[0])
    path = "./Shared/" + files[0]
    files.append(file_list[0])
    stat_info = os.stat(path)
    size = stat_info.st_size
    with open(path,'rb') as infile:
        while True:
            chunk = infile.read(CHUNKY_SIZE)
            chunks.append(chunk)
            if not chunk: break

def connect_tracker(ip,port,time):
    global peer
    # opens the socket to connect to the tracker
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connects to the server
    socket.connect((ip, port))
    socket.send(str(len(files)).encode())
    for i in files:
        socket.send(files[i].encode())
        socket.send(str(len(chunks)).encode())
    peer = socket.recv(1024).decode()


# Still need to figure out how to to the downloading
def put_together():
        # STITCH IMAGE BACK TOGETHER
    # Normally this will be in another location to stitch it back together
    read_file = open('chunkfile.txt', 'rb')

    # Create the jpg file
    file_name = ''
    with open('./Shared/'+ file_name, 'wb') as stitched:
        for f in read_file:
            stitched.write(f)

# To download the files from the P2P
def download():
    return

# Main function
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Missing parameters')
        exit()
    address = sys.argv[1]
    port = int(sys.argv[2])
    min_alive = int(sys.argv[3])
    process_file()
    connect_tracker(address,port,min_alive)
