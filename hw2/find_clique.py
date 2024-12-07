import time
import numpy as np
import re

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def greedy_randomize_clique(self, iterations: int=10):
        best_clique = []
        vertices_degrees = [(len(self.graph[i]), i) for i in range(self.V)]
        sorted_degrees = sorted(vertices_degrees, reverse=True)
        for count_n, vertex in sorted_degrees:
            if count_n <= len(best_clique):
                continue
            for _ in range(iterations):
                clique = [vertex]
                clique_candidates = self.graph[vertex]
                
                candidate_degrees = []
                for i in sorted_degrees:
                    if i[1] in clique_candidates:
                        candidate_degrees.append(i)

                for _, v_candidate in candidate_degrees:
                    flag = True
                    for v_clique in clique:
                        if v_candidate not in self.graph[v_clique]:
                            flag = False
                            break
                    if flag == True:
                        clique.append(v_candidate)

                if len(clique) > len(best_clique):
                    best_clique = clique
        return best_clique
    
def read_graph(filename):
    with open(filename, 'r') as file:
            for line in file:
                line = re.sub(" +", " ", line)
                line = line.rstrip().split(' ')
                if line[0] == "p":
                    count_vertex = int(line[2])
                    graph = Graph(count_vertex)
                if line[0] == "e":
                    graph.add_edge(int(line[1])-1, int(line[2])-1)  
    return graph

def check_results(graph, result):
    clique = [result[0]]

    for v_candidate in result[1:]:
        flag = True
        for v_clique in clique:
            if v_candidate not in graph[v_clique]:
                flag = False
                break
        if flag == True:
            clique.append(v_candidate)

    if len(result) == len(clique):
        return True
    else:
        return False


def save_results(filename, time_alg, result, graph):
    with open("result.txt", "a") as result_file:
        result_file.write(filename)
        result_file.write("\n")
        result_file.write(f'Time = {time_alg}')
        result_file.write("\n")
        result_file.write(f'Count colors: {len(set(result))}')
        result_file.write("\n")
        result_file.write(str(result))
        result_file.write("\n")
        result_file.write(f'Is correct clique = {check_results(graph.graph, result)}')
        result_file.write("\n\n")


files = ["brock200_1", "brock200_2", "brock200_3", "brock200_4", "brock400_1", "brock400_2","brock400_3","brock400_4"
    ,"C125.9", "gen200_p0.9_44","gen200_p0.9_55", "hamming8-4","johnson8-2-4", "johnson16-2-4", "keller4","MANN_a27", 
    "MANN_a9", "p_hat1000-1", "p_hat1000-2","p_hat1500-1","p_hat300-3", "p_hat500-3", "san1000", "sanr200_0.9", "sanr400_0.7"]

for filename in files:
    graph = read_graph(f'test_data/{filename}.clq')
    start = time.time()
    result = graph.greedy_randomize_clique()
    end = time.time()
    time_alg = end - start
    save_results(filename, time_alg, result, graph)
