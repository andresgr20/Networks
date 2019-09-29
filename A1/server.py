#!/usr/bin/env python3

import socket,sys

if len(sys.argv) != 2:
    print('Missing the req_code')
    exit()
code = str(sys.argv[1])

# port for the server
serverPort = 2019
negPort = 65534

while True:
    #Validation UTP protocol connection
    valSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    valSocket.bind(('localhost', serverPort))
    # listen sets the number of active clients for the server
    # set to 10 for testing
    valSocket.listen(10)
    print('The server is waiting for the client to connect')
    connectionSocket, addr = valSocket.accept()
    msg = connectionSocket.recv(1024).decode()
    # Terminates the connection if the user enters TERMINATE
    if( msg != code):
        response = '0'
        connectionSocket.send(response.encode())
        print('Invalid req_code from the user.Retry again')
    else:
        connectionSocket.send(negPort.encode())
        # Increases the negotation port of the clients
        negPort=+1
        connectionSocket.close()

        # sets the socket to udp protocol
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DTREAM)
        serverSocket.bind(('localhost', negPort))
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
                    connectionSocket.send("NO MSG.")
            # Terminates the connection if the user enters TERMINATE
            if( 'TERMINATE' in msg):
                connectionSocket.send('Shutting down server')
                print('Server shut down')
                connectionSocket.close()
                exit()
            # Maintains a list of the stored msgs
            msgs.append(msg)
            # Maintains a list of the active clients
            clients.append(connectionSocket)
            connectionSocket.close()

def broadcast_msg(msg, connection):
    for client in clients:
        if client != connection:
            try: 
                client.send(msg)
            except:
                client.close()
                # removes the clients that exited the server
                clients.remove(client)
