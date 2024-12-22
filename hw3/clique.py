import time
import random
import re
import numpy as np

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
        self.best_clique_size = 0

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def get_neighbors(self, v):
        return self.graph[v]
    
    def grasp(self, iterations: int=5000):
        best_clique = []
        for _ in range(iterations):
            vertex = np.random.choice(self.V)
            clique = [vertex]
            clique_candidates = self.graph[vertex]
            np.random.shuffle(clique_candidates)
            
            for v_candidate in clique_candidates:
                flag = True
                for v_clique in clique:
                    if v_candidate not in self.graph[v_clique]:
                        flag = False
                        break
                if flag == True:
                    clique.append(v_candidate)

            clique = self.local_search(clique)

            if len(clique) > len(best_clique):
                best_clique = clique
                self.best_clique_size = len(clique)
       
        return best_clique


    def local_search(self, solution):
        best_solution = solution.copy()

        for _ in range(5):
            for i in range(3):
                if len(solution) == 0:
                    break
                el_del = np.random.choice(solution)
                solution.remove(el_del)
            
            candidates = []
            for i in range(self.V):
                if all(element in self.graph[i] for element in solution) and i not in solution:
                    candidates.append(i)

            if (len(candidates)) == 0 or len(candidates) + len(solution) <= self.best_clique_size:
                return best_solution
            
            start_v = random.choices(candidates)[0]
            solution_cp = solution.copy()
            candidates_cp = candidates.copy()
            solution_cp.append(start_v) 
            candidates_cp.remove(start_v)
            np.random.shuffle(candidates_cp)
            for v_candidate in candidates_cp:
                flag = True
                for v_clique in solution_cp:
                    if v_candidate not in self.graph[v_clique]:
                        flag = False
                        break
                if flag == True:
                    solution_cp.append(v_candidate)

            if len(solution_cp) > len(best_solution):
                best_solution = solution_cp
      
        return best_solution
    
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
        result_file.write(f'Clique size: {len(set(result))}')
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
    result = graph.grasp()
    end = time.time()
    time_alg = end - start
    save_results(filename, time_alg, result, graph)
