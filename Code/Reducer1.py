#!/usr/bin/env python

# -*- coding: utf-8 -*-
#reducer1.py

import sys
#import time
import numpy as np

SEP = "," #easy to change separator

class Reducer1(object):
    
    def __init__(self, stream, sep=SEP):
        self.stream = stream
        self.sep = SEP
        
    def emit(self, key, value):
        sys.stdout.write("({0}{1}{2})\n".format(key, self.sep, value))     
    
    def reducer1_emit_len2_paths(self):
        for line in self: # was self.stream before
            try:
                #parts = line.split(self.sep) #doing this on a gutty thought
                vertex = line[0]#parts[0]
                neighbors = line[1]
                if len(neighbors) >= 2:
                    for i in range(len(neighbors)-1):
                        self.emit(vertex, [neighbors[i], neighbors[i+1]])
                else:
                    pass
            except:
                continue

if __name__ == "__main__":
    reducer = Reducer1(sys.stdin)
    reducer.reducer1_emit_len2_paths()