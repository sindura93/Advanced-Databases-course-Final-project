#!/usr/bin/env python

# -*- coding: utf-8 -*-
#mapper1.py

import sys
#import time
#import numpy as np


SEP = "," #easy to change separator

class Mapper2(object):
    
    def __init__(self, edges_file, stream, sep=SEP):
        self.edges_file = edges_file
        self.stream = stream
        self.sep = SEP
        
    def emit(self, key, value):
        sys.stdout.write("({0}{1}{2})\n".format(key, self.sep, value))
    
    def mapper2_emit_uvwdoll(self):
        edges = open(self.edges_file, "r")
        lines = edges.readlines()
        E_list = []
        
        for i in range(len(lines)):
            tmp = lines[i].split(self.sep)
            E_list.append((int(tmp[0]),int(tmp[1])))
            E_list.append((int(tmp[1]),int(tmp[0])))            
        
        for line in self:
            try:
                vertex = line[0]
                neighbors = line[1]
                v1 = neighbors[0]
                v2 = neighbors[1]
                
                if (v1,v2) in E_list:
                    self.emit((v1,v2),vertex)
                    self.emit((v1,v2),"$")       
            except:
                continue



if __name__ == "__main__":
    mapper = Mapper2(sys.stdin)
    mapper.mapper2_emit_uvwdoll()

