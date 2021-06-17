# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 06:33:58 2019

@author: sindu
"""
import sys
import numpy as np
import time

filename = "Weather_1000"#"Light_100"#"Graph_Sample9.txt" #"Light_100"
SEP = "," #easy to change separator

start_time = time.time()

def mapper1_emit_uv(file_name):
    graph_file = open(file_name, "r")
    lines = graph_file.readlines()
    v_count = int(lines[1])
    e_count = int(lines[2])
    V_list = []
    E_list = []
    edge_start_index = 3 + v_count
    
    node_neighbor_matrix = np.asmatrix(np.zeros([v_count+1,v_count+1]))
    node_degree_matrix = np.matrix(np.zeros([v_count+1,1]))
    
    u_v_list = []
    
    if v_count > 2:
        for i in range(v_count):
            V_list.append(int(lines[3+i]))
            
        for j in range(edge_start_index, edge_start_index + e_count):
            tmp = lines[j].split(",")
            E_list.append((int(tmp[0]),int(tmp[1])))
            E_list.append((int(tmp[1]),int(tmp[0])))            
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
            #self.emit(v,u_list)
            
            u_v_list.append((v, u_list))
    #print(node_degree_matrix)
    print("Mapper1 o/p:\n")
    print(len(u_v_list))
    
    return u_v_list
            
def reducer1_emit_len2_paths(stream):
    u_v1_v2_list = []
    for line in stream:
        try:
            #parts = line.split(sep)
            vertex = line[0]
            neighbors = line[1]
#                if len(neighbors) == 2:
#                    self.emit(vertex, neighbors)
            if len(neighbors) >= 2:
                for i in range(len(neighbors)-1):
                    #self.emit(vertex, [neighbors[i], neighbors[i+1]])
                    u_v1_v2_list.append((vertex, [neighbors[i], neighbors[i+1]]))
            else:
                pass
        except:
            continue
    print("\nReducer1 o/p:\n")
    print(len(u_v1_v2_list))
    return u_v1_v2_list


def mapper2_emit_uvwdoll(edges_file, uvlist):
    edges = open(edges_file, "r")
    lines = edges.readlines()
    E_list = []
    uvwdoll_list = []
    
    for i in range(len(lines)):
        tmp = lines[i].split(SEP)
        E_list.append((int(tmp[0]),int(tmp[1])))
        E_list.append((int(tmp[1]),int(tmp[0])))            
    
    for line in uvlist:
        try:
            vertex = line[0]
            neighbors = line[1]
            v1 = neighbors[0]
            v2 = neighbors[1]
            
            if (v1,v2) in E_list:
                #self.emit((v1,v2),vertex)
                #self.emit((v1,v2),"$")
                uvwdoll_list.append(((v1,v2),vertex))
                uvwdoll_list.append(((v1,v2),"$"))
        except:
            continue
    print("\nMapper2 o/p:\n")
    print(len(uvwdoll_list))
    return uvwdoll_list


def reducer2_count_triangles(finalist):
    triangle_count = 0
    v1v2_udollar_dict = {}
    for line in finalist: # was self.stream before
        try:
            v1v2 = line[0]
            u_dollar = line[1]
            
            if v1v2 in v1v2_udollar_dict.keys():
                dictval = v1v2_udollar_dict[v1v2]
                if type(dictval) == list:
                    tmplist = v1v2_udollar_dict[v1v2]
                    if u_dollar not in tmplist:
                        tmplist.append(u_dollar)
                        v1v2_udollar_dict[v1v2] = tmplist
                elif (type(dictval) == int or type(dictval) == str) and dictval != u_dollar:
                    tmplist = []
                    tmplist.append(dictval)
                    tmplist.append(str(u_dollar))
                    v1v2_udollar_dict[v1v2] = tmplist
            else:
                v1v2_udollar_dict[v1v2] = u_dollar
        except:
            continue
    
    print("\nReducer2 dict o/p:\n")
    print(len(v1v2_udollar_dict))
    for key, val in v1v2_udollar_dict.items():
        #print(key)
        #print(val)
        if '$' in val:
            total_vertices_count = len(val) - 1 # 2 for the vertices in key
            count = (total_vertices_count)
            triangle_count = triangle_count + count
    
    print(triangle_count)
    return triangle_count


mapper1 = mapper1_emit_uv(filename)

reducer1 = reducer1_emit_len2_paths(mapper1)

mapper2 = mapper2_emit_uvwdoll("Weather_1000_edges.txt", reducer1)
#mapper2 = mapper2_emit_uvwdoll("Graph_Sample9_edges.txt", reducer1)

reducer2 = reducer2_count_triangles(mapper2)

print("--- %s seconds ---" % (time.time() - start_time))
