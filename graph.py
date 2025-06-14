class Graph:
    def __init__(self):
        self.vertices = {}

    def addVertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = set()
            print(f"Vertex '{vertex}' added to the graph.")
        else:
            print(f"Vertex '{vertex}' already exists in the graph.")

    def addEdge(self, from_vertex, to_vertex):
        if from_vertex in self.vertices and to_vertex in self.vertices:
            self.vertices[from_vertex].add(to_vertex)
            print(f"Edge added from '{from_vertex}' to '{to_vertex}'.")
        else:
            print(f"Error: One or both vertices ('{from_vertex}', '{to_vertex}') not found. Cannot add edge.")

    def listOutgoingAdjacentVertex(self, vertex):
        if vertex in self.vertices:
            return self.vertices[vertex]
        else:
            print(f"Vertex '{vertex}' not found in the graph.")
            return set()

    def removeEdge(self, from_vertex, to_vertex):
        if from_vertex in self.vertices and to_vertex in self.vertices[from_vertex]:
            self.vertices[from_vertex].remove(to_vertex)
            print(f"Edge removed from '{from_vertex}' to '{to_vertex}'.")
        else:
            print(f"Error: Edge from '{from_vertex}' to '{to_vertex}' does not exist or vertices not found.")

    def get_all_vertices(self):
        return list(self.vertices.keys())