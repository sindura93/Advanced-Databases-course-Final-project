from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import sys

SEP = ","
class MRNodeIteratorPlus(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_emit_uv,
                   combiner=self.combiner_count_uv,
                   reducer=self.reducer_emit_len2_paths),
            MRStep(mapper=self.mapper_emit_uvwdoll,
                   combiner=self.combiner_count_uvwdoll,
                   reducer=self.reducer_count_triangles)
        ]

    def mapper_emit_uv(self, filename):
        graph_file = open(filename, "r")
        lines = graph_file.readlines()
        v_count = int(lines[1])
        e_count = int(lines[2])
        V_list = []
        edge_start_index = 3 + v_count
        node_neighbor_matrix = np.asmatrix(np.zeros([v_count + 1, v_count + 1]))
        node_degree_matrix = np.matrix(np.zeros([v_count + 1, 1]))

        if v_count > 2:
            for i in range(v_count):
                V_list.append(int(lines[3 + i]))

            for j in range(edge_start_index, edge_start_index + e_count):
                tmp = lines[j].split(SEP)
                node_neighbor_matrix[int(tmp[0]), int(tmp[1])] = 1
                node_neighbor_matrix[int(tmp[1]), int(tmp[0])] = 1

            node_degree_matrix = np.sum(node_neighbor_matrix, 1)

            for v in V_list:
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

    def reducer_emit_len2_paths(self, stream):
        for line in stream: # was self.stream before
            #try:
            parts = line.split(SEP) #doing this on a gutty thought
            vertex = line[0]#parts[0]
            neighbors = line[1]
            if len(neighbors) >= 2:
                for i in range(len(neighbors)-1):
                    #self.emit(vertex, [neighbors[i], neighbors[i+1]])
                    yield (vertex, [neighbors[i], neighbors[i+1]])
            else:
                pass
            #except:
             #   continue

    def mapper_emit_uvwdoll(self):
        pass

    def combiner_count_uvwdoll(self):
        pass

    def reducer_count_triangles(self):
        pass

    def mapper_get_words(self, _, line):
        # yield each word in the line
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner_count_words(self, word, counts):
        # optimization: sum the words we've seen so far
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function.
        yield None, (sum(counts), word)

    # discard the key; it is just None
    def reducer_find_max_word(self, _, word_count_pairs):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        yield max(word_count_pairs)

if __name__ == "__main__":
    MRNodeIteratorPlus.run()