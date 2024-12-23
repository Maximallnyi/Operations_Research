import time
import random
import re
import numpy as np

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]
        self.best_clique = []
        self.curr_clique = []
        self.time_start = None

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def get_neighbors(self, v):
        return self.graph[v]
    
    def grasp(self, iterations: int=100):
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

        for _ in range(3):
            for i in range(2):
                if len(solution) == 0:
                    break
                el_del = np.random.choice(solution)
                solution.remove(el_del)
            
            candidates = []
            for i in range(self.V):
                if all(element in self.graph[i] for element in solution) and i not in solution:
                    candidates.append(i)

            if (len(candidates)) == 0 or len(candidates) + len(solution) <= len(self.best_clique):
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

    def bnb(self, max_time):
        self.best_clique = self.grasp()
        candidates = [i for i in range(self.V)]
        np.random.shuffle(candidates)
        self.time_start = time.time()
        result = self.bnb_recurs(candidates, max_time)
        return result
    
    def bnb_recurs(self, candidates, max_time):
        if time.time() - self.time_start > max_time:
            return False
        
        if not candidates:
            if len(self.curr_clique) > len(self.best_clique):
                self.best_clique = self.curr_clique.copy()
            return
        
        if len(self.curr_clique) + len(candidates) <= len(self.best_clique):
            return

        for vertex in range(len(candidates)):
            self.curr_clique.append(candidates[vertex])
            new_candidates = []
            for other_vertex in range(vertex, len(candidates)):
                if candidates[other_vertex] in self.graph[candidates[vertex]]:
                    new_candidates.append(candidates[other_vertex])
            self.bnb_recurs(new_candidates, max_time)
            self.curr_clique.remove(candidates[vertex])

        return self.best_clique

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


files = ["brock200_2", "brock200_3", "brock200_4", "hamming8-4","johnson8-2-4", "johnson16-2-4", "keller4", "MANN_a9"]

for filename in files:
    graph = read_graph(f'test_data/{filename}.clq')
    start = time.time()
    result = graph.bnb(300)
    print(result)
    end = time.time()
    time_alg = end - start
    save_results(filename, time_alg, result, graph)
