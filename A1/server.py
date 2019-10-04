#!/usr/bin/env python3

import socket,sys,_thread, threading, random

# port for the server
serverPort = 20238
# create a random port number for the neg
msgs = ['shi','no']
clients = []

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
            negPort = randomize()
            _thread.start_new_thread(bootup_server,(valSocket,code,))
            connectionSocket.send(str(negPort).encode())
            # sets the socket to udp protocol
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serverSocket.bind(('localhost', negPort))
            print('The server is ready to receive messages')
            print(negPort)
            while True:
                #Since we are using UDP, recvfrom would be the correct way to
                # accept the connection
                msg, clientAddress= serverSocket.recvfrom(2048)
                serverMsg = 'NO MSG.'
                if(msg.decode() == 'GET'):
                    for x in msgs:
                        print(x)
                        single = str(x).encode()
                        serverSocket.sendto(single,clientAddress)
                    # send the msg that we have no more messages
                    serverSocket.sendto(serverMsg.encode(),clientAddress)
                else:            
                    # Maintains a list of the stored msgs
                    msgs.append(msg)
                    print(msgs)
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


def main():
    if len(sys.argv) != 2:
        print('Missing the req_code')
        exit()
    code = sys.argv[1]
    negPort = randomize()
    #Validation UTP protocol connection
    valSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # valSocket.setblocking(0)
    valSocket.bind(('localhost', serverPort))
    bootup_server(valSocket,code)
    valSocket.close()

main()

# #!/usr/bin/env python3

# import socket,sys,_thread, random,traceback
# from threading import Thread

# # port for the server
# serverPort = 20238
# # create a random port number for the negotiation port
# negPort = randomize()
# # array of messages stored
# msgs = []

# def randomize():
#     return random.randint(1025,65535)


# def bootup_verification_server(code,socket):
#     while True:
#         connectionSocket, addr = socket.accept()
#         msg = connectionSocket.recv(1024).decode()
#         # If the clients sends the incorrect req_code, deny connection
#     if( msg != code):
#         response = '0'
#         connectionSocket.send(response.encode())
#         print('Invalid req_code from the client. Retry again')
#     else:
#         try:
#             _thread.start_new_thread(bootup_verification_server,(code,socket,))
#             connectionSocket.send(str(negPort).encode())
#             socket.close()
#         except:
#             print("Thread did not start")

# def chatbot_server_bootup():
#     print('The server is waiting for the client to connect')
#     # sets the socket to udp protocol
#     serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     serverSocket.bind(('localhost', negPort))
#     negPort=randomize()
#     print('The server is ready to receive messages')
#     while True:
#     #Since we are using UDP, recvfrom would be the correct way to
#     # accept the connection
#         msg, clientAddress= serverSocket.recvfrom(2048)
#         serverMsg = 'NO MSG.'
#         if(msg.decode() == 'GET'):
#             for x in msgs:
#                 print(x)
#                 serverSocket.sendto(x.encode(),clientAddress)
#                 # send the msg that we have no more messages
#                 serverSocket.sendto(serverMsg.encode(),clientAddress)
#         else:            
#             # Maintains a list of the stored msgs
#             msgs.append(msg)
#             print(msgs)
#         # Terminates the connection if the user enters TERMINATE
#         if( 'TERMINATE' in msg.decode()):
#             serverMsg = 'Shutting down server'
#             serverSocket.sendto(serverMsg.encode(),clientAddress)
#             print('Server shut down')
#             serverSocket.close()
#             exit()
#     serverSocket.close()

# def main():
#     if len(sys.argv) != 2:
#         print('Missing the req_code')
#         exit()
#     code = sys.argv[1]
#     #Validation UTP protocol connection
#     valSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     valSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     # valSocket.setblocking(0)
#     valSocket.bind(('localhost', serverPort))
#     # listen sets the number of active clients for the server
#     # set to 10 for testing
#     valSocket.listen(10)
#     bootup_verification_server(code,valSocket)
#     chatbot_server_bootup(negPort)
    
