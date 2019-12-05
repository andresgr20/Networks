#!/usr/bin/env python3

import socket,sys,_thread, random, threading,os, pickle, struct

# Max number of threads that will be stored
N = 24
CHUNKY_SIZE = 512
chunks = []
files = []
size_file = 0

#Peer ID
peer = 0

flag = True
def run_timer(t,s):
    # Timer 
    # need to figure out how to get the flag
    # While loop
    # keep waiitng for message
    timer = threading.Timer(t, exit_peer(s))
    timer.start()
    while True:
        d = s.recv(1024).decode()
        if(d == '200'):
            timer.cancel()
            break
            print('Timer cancelled')

def exit_peer(s):
    s.send()
    print('PEER ' + str(peer) + ' SHUTDOWN: HAS ' + str(len(files)))
    for i in files:
        print(str(peer) + '    ' + i)
    exit()

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


# Obtains the chunks and the size of the file
def process_file():
    global size_file
    file_list =  os.listdir("./Shared")
    files.append(file_list[0])
    path = "./Shared/" + files[0]
    stat_info = os.stat(path)
    size_file = stat_info.st_size
    with open(path,'rb') as infile:
        while True:
            chunk = infile.read(CHUNKY_SIZE)
            chunks.append(chunk)
            if not chunk: break
    
def connect_tracker(ip,port):
    global peer
    # client to get the negotation port for the server UTP
    trackerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connects to the server
    trackerSocket.connect((ip, port))
    peer = trackerSocket.recv(1024).decode()
    data = [len(files),files[0],size_file,len(chunks),ip,port]
    # data_string = pickle.dumps(data)
    # trackerSocket.send(data_string)
    for i in data:
        trackerSocket.send(str(i).encode())
    return trackerSocket

# Still need to figure out how to to the downloading
def put_together(data,name):
    # STITCH IMAGE BACK TOGETHER
    # Normally this will be in another location to stitch it back together
    # read_file = open(name, 'wb')  May have to turn the data in that if it is not working
    with open('./Shared/'+ name, 'wb') as stitched:
        for f in data:
            stitched.write(f)

# To download the files from the P2P
def downloadClient(ip,port,chunk_no):
    # UDP for the chunks info here
    downloadSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    downloadSocket.connect(ip,port)
    for i in chunks:
        downloadSocket.send(i.encode())
    downloadSocket.close()

# Downloads the files 
def downloadServer(ip,port,chunk_no,s):
    downloadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    downloadSocket.bind((ip, port))
    connectionSocket, addr = downloadSocket.accept()
    new_file = []
    chunk_count = 0
    while True:
        d = connectionSocket.recv(512).decode()
        chunk_count += 1  
        if not d: break
        new_file.append(d)
        process  = chunk_count/chunk_no
        # Push of the process of the download
        if(process == .25 or process == .50  or process == .75 or process == 1):
            s.send(str(peer).encode())
            s.send(str(chunk_count).encode())
    connectionSocket.close()
    downloadSocket.close()
    put_together(new_file)


# Main function
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Missing parameters')
        exit()
    address = sys.argv[1]
    port = int(sys.argv[2])
    min_alive = int(sys.argv[3])
    process_file()
    trackerSocket = connect_tracker(address,port)
    # The timer needs to be in a loop that will be trigger from a flag that is blocked from downloading
    # run_timer(min_alive, trackerSocket)
    print("exit")
    # run_timer(min_alive)
    # s=connect_tracker(address,port,min_alive)

