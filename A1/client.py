#!/usr/bin/env python3

import socket,sys

# Gets the arguments from the script
if len(sys.argv) != 5:
    print('Missing arguments! Script, servers address, port, req_code, message')
    exit()
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
code = str(sys.argv[3])
input_msg = str(sys.argv[4])

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

# verfied socket client after negotiation UDP
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSocket.connect((serverName,port))
msg = "GET"
clientSocket.send(msg.encode())
msgs = clientSocket.recv(1024).decode()
# print the messages on different lines
print ('\n').join(str(m) for m in msgs)
# Sends the server the current port as part of a string 
msg = '['+str(port)+']: '+ input_msg
clientSocket.send(msg.encode())

while True:
    ex = raw_input('Press any key to exit.')
    if(ex != ''):
        clientSocket.close()
        exit()
clientSocket.close()