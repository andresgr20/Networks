#!/usr/bin/env python

import socket,sys

if len(sys.argv) != 2:
    print('Missing the req_code')
    exit()
code = int(sys.argv[1])

# port for the server
serverPort = 12000
negPort = 65534

#Validation UTP protocol connection
valSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
valSocket.bind(('localhost', serverPort))
# listen sets the number of active clients for the server
# set to 10 for testing
valSocket.listen(10)
print('The server is waiting for the req_code')
connectionSocket, addr = valSocket.accept()
msg = connectionSocket.recv(1024).decode()
# Terminates the connection if the user enters TERMINATE
if( msg != code):
    connectionSocket.send('0')
    print('Invalid req_code')
else:
    connectionSocket.send(negPort)
    negPort=+1
    connectionSocket.close()

    # sets the socket to udp protocol
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DTREAM)
    serverSocket.bind(('localhost', serverPort))
    # listen sets the number of active clients for the server
    # set to 10 for testing
    serverSocket.listen(10)
    print('The server is ready to receive messages')
    msgs = []
    clients = []
    while True:
        connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode()
        if(msg == "GET"):
            if not msgs: #If there are no messages stored
                connectionSocket.send("NO MSG")
        # Terminates the connection if the user enters TERMINATE
        if( msg == 'TERMINATE'):
            connectionSocket.send('Shutting down server')
            print('Server shut down')
            connectionSocket.close()
            exit()
        msgs.append(msg)
        connectionSocket.send('Client 1 Message:'+ msg.encode())
        connectionSocket.close()