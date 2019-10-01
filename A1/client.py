#!/usr/bin/env python3

import socket,sys,_thread

# Gets the arguments from the script
if len(sys.argv) != 5:
    print('Missing arguments! Script, servers address, port, req_code, message')
    exit()
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])
code = sys.argv[3]
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
print('Connected with authentication')
clientSocket.send(msg.encode())
msgs = ''
while True:
    msgs = clientSocket.recv(2048).decode()
    # flag to know that we have to more messages to receive
    if(msgs == 'end'):
        break
    print(msgs)
# print the messages on different lines
# Sends the server the current port as part of a string 
msg = '['+str(port)+']: '+ input_msg
clientSocket.send(msg.encode())

while True:
    ex = input('Press any key to exit.')
    clientSocket.close()
    exit()
clientSocket.close()