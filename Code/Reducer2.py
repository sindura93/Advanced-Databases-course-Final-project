#!/usr/bin/env python

# -*- coding: utf-8 -*-
#mapper1.py

import sys
#import time
#import numpy as np


SEP = "," #easy to change separator

class Reducer2(object):
    
    def __init__(self, stream, sep=SEP):
        self.stream = stream
        self.sep = SEP
        
    def emit(self, key, value):
        sys.stdout.write("({0}{1}{2})\n".format(key, self.sep, value))     
    
    def reducer2_count_triangles(self):
        triangle_count = 0
        v1v2_udollar_dict = {}
        for line in self: # was self.stream before
            try:
                #parts = line.split(self.sep) #doing this on a gutty thought
                v1v2 = line[0]#parts[0]
                u_dollar = line[1] #this as in u or dollar sign
                if v1v2 in v1v2_udollar_dict.keys():
                    if len(v1v2_udollar_dict[v1v2]) > 1:
                        tmplist = v1v2_udollar_dict[v1v2]
                        if u_dollar not in tmplist:
                            tmplist = tmplist.append(u_dollar)
                            v1v2_udollar_dict[v1v2] = tmplist
                    elif len(v1v2_udollar_dict[v1v2]) == 1 and v1v2_udollar_dict[v1v2] != u_dollar:
                        tmplist = []
                        tmplist = tmplist.append(v1v2_udollar_dict[v1v2])
                        tmplist = tmplist.append(u_dollar)
                        v1v2_udollar_dict[v1v2] = tmplist
                else:
                    v1v2_udollar_dict[v1v2] = u_dollar
            except:
                continue
            
        for key,val in v1v2_udollar_dict:
            if "$" in val:
                total_vertices_count = 2 + len(val) - 1 # 2 for the vertices in key
                count = (total_vertices_count)/3
                triangle_count = triangle_count + count
                        

if __name__ == "__main__":
    reducer = Reducer2(sys.stdin)
    reducer.reducer2_count_triangles()