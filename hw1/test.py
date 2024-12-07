import time

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def greedy_coloring(self):
        color_map = {}
        color_dict = {}
        vertices_degrees = [(len(self.graph[i]), i) for i in range(self.V)]
        vertices_degrees.sort(reverse=True)
        
        for _, vertex in vertices_degrees:
            n_colors = {color_map.get(n) for n in self.graph[vertex]}
            c = next(color for color in range(self.V) if color not in n_colors)
            color_map[vertex] = c
            if c not in color_dict:
                color_dict[c] = [vertex]
            else:
                color_dict[c].append(vertex)
            
        return color_dict
    
def read_graph(filename):
    with open(filename, 'r') as file:
            for line in file:
                line = line.rstrip().split(' ')
                if line[0] == "p":
                    count_vertex = int(line[2])
                    graph = Graph(count_vertex)
                if line[0] == "e":
                    graph.add_edge(int(line[1])-1, int(line[2])-1)  
    return graph       

def check_results(graph, result):
    for i in result:
        for j in range(len(result[i])):
            for k in range(j+1, len(result[i])):
                if result[i][k] in graph[result[i][j]]:
                    return False
    return True

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
        result_file.write(f'Is correct colors = {check_results(graph.graph, result)}')
        result_file.write("\n\n")

files = ["myciel3.col", "myciel7.col", "school1.col", "school1_nsh.col",
                 "anna.col", "miles1000.col","miles1500.col", "le450_5a.col", "le450_15b.col", "queen11_11.col"]

for filename in files:
    graph = read_graph(f'test_data/{filename}')
    start = time.time()
    result = graph.greedy_coloring()
    end = time.time()
    time_alg = end - start
    save_results(filename, time_alg, result, graph)