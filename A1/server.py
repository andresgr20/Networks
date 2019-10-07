#!/usr/bin/env python

import socket,sys,thread, random, threading,os

# port for the server
serverPort = 20238
# create a random port number for the neg
msgs = []


# creates a random number to find the port
def randomize():
    return random.randint(1025,65535)

def bootup_server(valSocket, code):
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
            # creates a port number
            negPort = randomize()
            # creates another thread if we have other users trying to obtain the resources
            thread.start_new_thread(bootup_server,(valSocket,code,))
            #sends the port number to the client
            connectionSocket.send(str(negPort).encode())
            # sets the socket to udp protocol
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serverSocket.bind(('localhost', negPort))
            print('The server is ready to receive messages')
            while True:
                # Since we are using UDP, recvfrom would be the correct way to
                # accept the connection
                msg, clientAddress= serverSocket.recvfrom(2048)
                serverMsg = 'NO MSG.'
                msg = msg.decode()
                if(msg == 'GET'):
                    for x in msgs:
                        single = str(x).encode()
                        serverSocket.sendto(single,clientAddress)
                    # send the msg that we have no more messages
                    serverSocket.sendto(serverMsg.encode(),clientAddress)
                else:            
                    # Maintains a list of the stored msgs
                    msgs.append(msg)
                # Terminates the connection if the user enters TERMINATE
                if( 'TERMINATE' in msg):
                    print('Server shut down')
                    connectionSocket.close()
                    exit()
                connectionSocket.close()


def main():
    if len(sys.argv) != 2:
        print('Missing the req_code')
        exit()
    code = sys.argv[1]
    negPort = randomize()
    #Validation UTP protocol connection
    valSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    valSocket.bind(('localhost', serverPort))
    bootup_server(valSocket,code)
    valSocket.close()

main()

