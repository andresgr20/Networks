#!/usr/bin/env python

import socket,sys

# if len(sys.argv) != 5:
#     print('Missing arguments! Script, servers address, port, req_code, message')
#     exit()
# serverName = str(sys.argv[1])
# port = int(sys.argv[2])
# code = int(sys.argv[3])
# msg = str(sys.argv[4])
serverName = 'localhost'
serverPort = 12000
code = 30
# client to get the negotation port for the server UTP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(code.encode())
response = clientSocket.recv(1024).decode()

#check if the validation from the server
if(response == '0'):
    print('Invalid req_code')
    clientSocket.close()
    exit()

# change the port to the one given by the server
port = int(response)
clientSocket.close()



sentence = raw_input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()