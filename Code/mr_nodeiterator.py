from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import sys

SEP = ","
#edgesfile = "Light_100_edges.txt"

class MRNodeIteratorP(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_emit_uv,
                   reducer=self.reducer_emit_len2_paths)
        ]

    def mapper_emit_uv(self, _, lines):
        #print(i for i in lines.split())
        #sys.stdout.write("({0})\n".format(lines.split()))
        #v_count = int(lines[1])
        #e_count = int(lines[2])
        #V_list = []
        #edge_start_index = 3 + v_count
        node_neighbor_matrix = np.asmatrix(np.zeros([5001, 5001]))
        node_degree_matrix = np.matrix(np.zeros([5001, 1]))

        for line in lines.split():
        #for j in range(edge_start_index, edge_start_index + e_count):
            tmp = line.split(SEP)
            node_neighbor_matrix[int(tmp[0]), int(tmp[1])] = 1
            node_neighbor_matrix[int(tmp[1]), int(tmp[0])] = 1

        node_degree_matrix = np.sum(node_neighbor_matrix, 1)

        for v in range(1,5001):
            v_degree = node_degree_matrix[v, 0]
            neighbors_arr = np.array(node_neighbor_matrix[v, :])
            # gets the indices that are basically neighbors of a vertex
            r1, neighbors = np.where(neighbors_arr == 1)
            u_list = []
            for neighbor1 in neighbors:
                neighbor1_degree = node_degree_matrix[neighbor1, 0]
                if neighbor1_degree > v_degree:
                    u = neighbor1
                    u_list.append(u)
            yield (v, u_list)



    #def combiner_count_uv(self):
        #pass

    def reducer_emit_len2_paths(self, vertex, neighbors):
        #for line in stream: # was self.stream before
            #try:
            #parts = line.split(SEP) #doing this on a gutty thought
            #vertex = line[0]#parts[0]
            #neighbors = line[1]
        if len(list(neighbors)) >= 2:
            neighbor_list = list(neighbors)
            for i in range(len(neighbor_list)-1):
                yield (vertex, [neighbor_list[i], neighbor_list[i+1]])
        else:
            pass
            #except:
             #   continue


if __name__ == "__main__":
    MRNodeIteratorP.run()