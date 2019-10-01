#!/usr/bin/env python3

import socket,sys,_thread

if len(sys.argv) != 2:
    print('Missing the req_code')
    exit()
code = sys.argv[1]

# port for the server
serverPort = 20238
negPort = 1998

#Validation UTP protocol connection
valSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
valSocket.bind(('localhost', serverPort))
while True:
    # listen sets the number of active clients for the server
    # set to 10 for testing
    valSocket.listen(10)
    print('The server is waiting for the client to connect')
    connectionSocket, addr = valSocket.accept()
    msg = connectionSocket.recv(1024).decode()
    # If the clients sends the incorrect req_code, deny connection
    if( msg != code):
        response = '0'
        connectionSocket.send(response.encode())
        print('Invalid req_code from the client. Retry again')
    else:
        connectionSocket.send(str(negPort).encode())

        # sets the socket to udp protocol
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind(('localhost', negPort))
        negPort=+1
        print('The server is ready to receive messages')
        msgs = ['[323]: hi','NO MSG.']
        clients = []
        while True:
            #Since we are using UDP, recvfrom would be the correct way to
            # accept the connection
            msg, clientAddress= serverSocket.recvfrom(2048)
            serverMsg = 'NO MSG'
            if(msg.decode() == 'GET'):
                for x in msgs:
                    print(x)
                    serverSocket.sendto(x.encode(),clientAddress)
                # sends a flag to say that we do not have anymore messages stored
                end = 'end'
                serverSocket.sendto(end.encode(),clientAddress)
            else:            
                # Maintains a list of the stored msgs
                msgs.append(msg)
            # Terminates the connection if the user enters TERMINATE
            if( 'TERMINATE' in msg.decode()):
                serverMsg = 'Shutting down server'
                serverSocket.sendto(serverMsg.encode(),clientAddress)
                print('Server shut down')
                connectionSocket.close()
                exit()
            # Maintains a list of the active clients
            clients.append(clientAddress)
            connectionSocket.close()
valSocket.close()

def broadcast_msg(msg, connection):
    for client in clients:
        if client != connection:
            try: 
                client.send(msg)
            except:
                client.close()
                # removes the clients that exited the server
                clients.remove(client)
