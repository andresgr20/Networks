#!/usr/bin/env python3
#files.py
from chunk import Chunk

class Files:
    file_name = ""
    file_size = 0
    chunk_total = 0
    chunks = []

    def __init__(self,size,chunks_no,name,IP,port):
        self.size = size
        self.chunk_total = chunks_no
        self.file_name = name
        for i in range(chunks_no):
            self.chunks.append(Chunk(i,IP,port))

    def get_name(self):
        return self.file_name
    
    def get_size(self):
        return self.file_size

    def get_chunk_total(self):
        return self.chunk_total
    
    def get_size(self):
        return self.file_size


    def get_chunk(self,chunk):
        return self.chunks[chunk]

    def update_chunk(self,chunk):
        return self.chunk[chunk].update(chunk)
