#!/usr/bin/env python

# -*- coding: utf-8 -*-
#mapper1.py

import sys
#import time
import numpy as np

SEP = "," #easy to change separator

class Mapper1(object):
    
    def __init__(self, filename, sep=SEP):
        self.filename = filename
        self.sep = SEP
        
    def emit(self, key, value):
        sys.stdout.write("({0}{1}{2})\n".format(key, self.sep, value))
    
    def mapper1_emit_uv(self):
        graph_file = open(self.filename, "r")
        lines = graph_file.readlines()
        v_count = int(lines[1])
        e_count = int(lines[2])
        V_list = []
        #E_list = []
        edge_start_index = 3 + v_count
        
        node_neighbor_matrix = np.asmatrix(np.zeros([v_count+1,v_count+1]))
        node_degree_matrix = np.matrix(np.zeros([v_count+1,1]))
        
        u_v_list = []
        
        if v_count > 2:
            for i in range(v_count):
                V_list.append(int(lines[3+i]))
                
            for j in range(edge_start_index, edge_start_index + e_count):
                tmp = lines[j].split(self.sep)
                #E_list.append((int(tmp[0]),int(tmp[1])))
                #E_list.append((int(tmp[1]),int(tmp[0])))            
                node_neighbor_matrix[int(tmp[0]),int(tmp[1])] = 1
                node_neighbor_matrix[int(tmp[1]),int(tmp[0])] = 1
            
            node_degree_matrix = np.sum(node_neighbor_matrix,1)
            
            for v in V_list:
                v_degree = node_degree_matrix[v,0]
                neighbors_arr = np.array(node_neighbor_matrix[v,:])
                #gets the indices that are basically neighbors of a vertex
                r1,neighbors = np.where(neighbors_arr==1)
                u_list = []
                for neighbor1 in neighbors:
                    neighbor1_degree = node_degree_matrix[neighbor1,0]
                    if neighbor1_degree > v_degree:
                        u = neighbor1
                        u_list.append(u)
                self.emit(v,u_list)
                
                u_v_list.append((v, u_list))
                
        
        #print(u_v_list)



if __name__ == "__main__":
    mapper = Mapper1(sys.stdin)
    mapper.mapper1_emit_uv()