import graphlib
import graphviz as gv
#from lab1 import tramdata
import json
import sys
gv.render.engine = 'dot'


class Graph:
    def __init__(self, start=None, values = None, directed=False):
        self._adjlist = {}
        if values is None:
            values = {}
        self._valuelist = values
        self._isdirected = directed
   
    def vertices(self):
        return list(self._adjlist.keys())
    
    def edges(self):
        edges = set()
        for vertex, neighbors in self._adjlist.items():
            for neighbor in neighbors:
                edges.add((vertex, neighbor))
        return edges

    def neighbours(self,v):
        return self._adjlist.get(v, set())
    
    def add_edge(self,a,b):
        self.add_vertex(a)
        self.add_vertex(b)
        self._adjlist.setdefault(a, set()).add(b)           
        self._adjlist.setdefault(b, set()).add(a)

    def add_vertex(self,a):
        self._adjlist.setdefault(a, set())

    def is_directed(self):
        return self.is_directed
    
    def get_vertex_value(self, v):
        return self._valuelist.get(v, None)
    
    def set_vertex_value(self, v, x):
        self._valuelist[v] = x

    def __len__(self):
        return len(self._adjlist)

    def remove_ed(self, node1, node2):
        if node1 in self._adjlist and node2 in self._adjlist[node1]:
            self._adjlist[node1].remove(node2)
    
        if not self._isdirected and node2 in self._adjlist and node1 in self._adjlist[node2]:
            self._adjlist[node2].remove(node1)

    def remove_ver(self, node):
        if node in self._adjlist:
            del self._adjlist[node]

            for vertex, neighbors in self._adjlist.items():
                if node in neighbors:
                    neighbors.remove(node)


                    
    def adj_list(self):
        return self._adjlist



class WeightedGraph(Graph):
    g = Graph()  # Create an instance of the Graph class
    edges_list = g.edges()  # Call the edges method on the instance

    def __init__(self, start=None, directed=False):
        super().__init__(start=start, directed=directed)
        self._weight_matrix = {}
        self._edges_list = self.edges() 

        
        for edge in self._edges_list:
            self._weight_matrix[edge] = {}
            for stop in self._edges_list[edge]:
                temp_weight = {stop: 'none'}
                self._weight_matrix[edge].update(temp_weight)

    def set_weight(self, a, b, w):
        self._weight_matrix[a][b] = w

    def get_weight(self, a, b):
        return self._weight_matrix[a][b]

    def weights_all(self):
        return self._weight_matrix
    

def dijkstra_algorithm(graph, start_node, cost_func=lambda u, v: 1):
    vertices = graph.vertices()
    distances = {v: float('inf') for v in vertices}
    previous_nodes = {v: None for v in vertices}
    all_paths = {v: [] for v in vertices}

    distances[start_node] = 0
    unvisited_nodes = set(vertices)

    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda v: distances[v])
        unvisited_nodes.remove(current_node)

        neighbors = graph.neighbours(current_node)
        for neighbor in neighbors:
            edge_weight = cost_func(current_node, neighbor)
            if distances[current_node] + edge_weight < distances[neighbor]:
                if neighbor in distances:
                    distances[neighbor] = distances[current_node] + edge_weight
                    previous_nodes[neighbor] = current_node
                    all_paths[neighbor] = all_paths[current_node] + [neighbor]

    return distances, all_paths

def visualize_weighted(self, view='dot', name='mygraph.gv', node_colors={}, engine='dot'):
    dot = gv.Graph(engine)
    edges_list = Graph.edges(self)


    for edge in edges_list:
        source_node, target_node = edge
        edge_to_color = list(node_colors.keys())
        dot.node(str(source_node))
        dot.node(str(target_node))

        if str(source_node) in edge_to_color and str(target_node) in edge_to_color:
            dot.edge(str(source_node), str(target_node), color="orange")
        else:
            dot.edge(str(source_node), str(target_node))

    for node, color in node_colors.items():
        dot.node(str(node), fillcolor=color, style='filled')

    dot.render(name, view, format='png')



        #     if str(source_node) in edge_to_color and str(target_node) in edge_to_color:
        #     dot.edge(str(source_node), str(target_node), color="orange")
        # else:
        #     dot.edge(str(source_node), str(target_node))

    for node, color in node_colors.items():
        dot.node(str(node), fillcolor=color, style='filled')

    dot.render(name, view, format='png')

def view_shortest_path_weighted(graph, start, end, cost_func=lambda u, v: 1):
    distances, paths = dijkstra_algorithm(graph, start, cost_func)
    colormap = {str(v): 'orange' for v in paths[end]}
    start_color = {str(start): "red"}
    end_color = {str(end): "yellow"}
    colormap.update(start_color)
    colormap.update(end_color)
    visualize_weighted(graph, view='view', node_colors=colormap)




