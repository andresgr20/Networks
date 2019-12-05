#!/usr/bin/env python3

import socket,sys,_thread, random, threading,os, pickle

# Max number of threads that will be stored
N = 24
CHUNKY_SIZE = 512
chunks = []
files = []
size_file = 0

#Peer ID
peer = 0

flag = True
def run_timer(t):
    # Timer 
    # need to figure out how to get the flag
    # While loop
    # keep waiitng for message

    timer = threading.Timer(t, exit_peer)
    timer.start()
    # Socket with the push from the tracker
    if(flag == True):
        timer.cancel()
        print('Timer cancelled')

def exit_peer():
    print('PEER ' + str(peer) + ' SHUTDOWN: HAS ' + str(len(files)))
    for i in files:
        print(str(peer) + '    ' + i)
    
    os.sys.exit()

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
    print("No Chunks "+ str(len(chunks)))
    print("File size " + str(size_file))
    
def connect_tracker(ip,port,time):
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
    # # File count
    # trackerSocket.send(str(len(files)).encode())
    # #Name
    # trackerSocket.send(files[0].encode())
    # #Size
    # trackerSocket.send(str(size_file).encode())

    # for i in files:
    #     trackerSocket.send(files[i].encode())
    #     trackerSocket.send(str(len(chunks)).encode())



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
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # UDP for the chunks info here
    # function starts when the user connects to the server and we have a flag with a thread 
    # timer would be here
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
    exit_peer()
    # run_timer(min_alive)
    # s=connect_tracker(address,port,min_alive)

