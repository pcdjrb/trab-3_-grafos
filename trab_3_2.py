import networkx as nx
from time import time

def read_graph_from_file(file_path):
    with open(file_path, 'r') as file:
        num_nodes = int(file.readline().strip())
        graph = nx.DiGraph()

        for line in file:
            origin, destiny, weight = map(int, line.strip().split())
            graph.add_edge(origin, destiny, weight=weight)

    return graph

def ford_fulkerson(graph, source, sink):
    residual_graph = graph.copy()
    flow = {edge: 0 for edge in graph.edges}
    max_flow = 0

    while True:
        path, capacity = find_augmenting_path(residual_graph, source, sink)
        if not path:
            break

        max_flow += capacity

        for u, v in zip(path, path[1:]):
            if residual_graph.has_edge(u, v):
                residual_graph[u][v]['weight'] -= capacity
            else:
                residual_graph[v][u]['weight'] += capacity

            flow[(u, v)] += capacity

    return max_flow, flow





def find_augmenting_path(graph, source, sink):
    visited = {node: False for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    queue = [source]

    while queue:
        u = queue.pop(0)
        visited[u] = True

        for v, attr in graph[u].items():
            if not visited[v] and attr['weight'] > 0:
                parent[v] = u
                queue.append(v)

                if v == sink:
                    path = []
                    current = v
                    capacity = float('inf')

                    while current is not None:
                        path.insert(0, current)
                        if parent[current] is not None:
                            capacity = min(capacity, graph[parent[current]][current]['weight'])
                        current = parent[current]

                    return path, capacity

    return None, 0

def save_result_to_file(result_file, max_flow, time):
    with open(result_file, 'w') as file:
        file.write(f"Maximum Flow: {max_flow}\n")
        file.write(f"Time Elapsed: {time}")

if __name__ == "__main__":
    file_path = "graph2.txt"  
    result_file = "graph2_r.txt"         
    graph = read_graph_from_file(file_path)

    source = 1  
    sink = 2    

    start = round(time(),3)
    
    max_flow, flow = ford_fulkerson(graph, source, sink)

    end = round(time(),3)
    

    # Save the result to a file
    save_result_to_file(result_file, max_flow, end - start)



