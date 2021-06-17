# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 20:08:20 2019

@author: sindu
"""


import time
import numpy as np

def node_iterator_plus_v5(filename):
    start_time = time.time()
    ##### Section 1: build initial variables from the file received ######
    #graph_file = open("Graph_Sample4.txt", "r")
    graph_file = open(filename, "r")
    lines = graph_file.readlines()
    v_count = int(lines[1])
    e_count = int(lines[2])
    V_list = []
    E_list = []
    edges_weight_tuples_list = []
    edge_start_index = 3 + v_count
    
    node_neighbor_matrix = np.asmatrix(np.zeros([v_count+1,v_count+1]))
    node_degree_matrix = np.matrix(np.zeros([v_count+1,1]))
    
    triangle_count = 0
    ###### section 1 ends ###########
    
    ##### Section 2: this section below builds vertices, edges, neighbors and node degrees list #####
    if v_count > 2:
        for i in range(v_count):
            V_list.append(int(lines[3+i])) #adding each of vertices to vertex list
            #node_degree_dict[int(lines[3+i])] = 0 #initializing node degree list
            #node_neighbor_dict[int(lines[3+i])] = 0 #initializing node neighbor dict
        #print(node_degree_dict)
        #print("--- %s seconds ---" % (time.time() - start_time))
        for j in range(edge_start_index, edge_start_index + e_count):
            tmp = lines[j].split(",")
            # adding edges and their weights line as a tuple to edges_weight_tuples_list
            edges_weight_tuples_list.append((int(tmp[0]),int(tmp[1]),float(tmp[2])))
            # adding edges separately to a list in their directional order
            E_list.append((int(tmp[0]),int(tmp[1])))
            E_list.append((int(tmp[1]),int(tmp[0])))            
            node_neighbor_matrix[int(tmp[0]),int(tmp[1])] = 1
            node_neighbor_matrix[int(tmp[1]),int(tmp[0])] = 1
            #node_degree_matrix[int(tmp[0]),1] = node_degree_matrix[int(tmp[0]),1] + 1
            #node_degree_matrix[int(tmp[1]),1] = node_degree_matrix[int(tmp[1]),1] + 1
            
        node_degree_matrix = np.sum(node_neighbor_matrix,1)
        
        #print("--- %s seconds ---" % (time.time() - start_time))
        
        for v in V_list:
            v_degree = node_degree_matrix[v,0]
            neighbors_arr = np.array(node_neighbor_matrix[v,:])
            r1,neighbors = np.where(neighbors_arr==1) #gets the indices that are basically neighbors of a vertex
            
            for neighbor1 in neighbors:
                neighbor1_degree = node_degree_matrix[neighbor1,0]
                if neighbor1_degree > v_degree:
                    u = neighbor1
                    u_degree = neighbor1_degree
                    next_neighbors_arr = np.array([x for x in neighbors if x!=u])
                    
                    for neighbor2 in next_neighbors_arr:
                        neighbor2_degree = node_degree_matrix[neighbor2,0]
                        if neighbor2_degree > u_degree:
                            w = neighbor2
                            w_degree = neighbor2_degree
                            
                            if (u,w) in E_list:
                                triangle_count = triangle_count + 1
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
            
            #print("vertex: ",v," | triangle_count: ",triangle_count)
           
        
        print("--- %s seconds ---" % (time.time() - start_time))
    
    print("triangle_count: ",triangle_count)
    return triangle_count