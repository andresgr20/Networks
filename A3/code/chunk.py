#!/usr/bin/env python3
#files.py


class Chunk:
    chunk_no = 1
    peers = []

    def __init__(self,chunk,IP,port):
        self.chunk_no = chunk
        self.peers.append([IP,port])
    
    def add(self,IP, port):
        self.peers.append([IP,port])
    
    def delete(self,IP,port):
        self.peers.remove([IP,port])

    def who(self):
        return self.peers
    
