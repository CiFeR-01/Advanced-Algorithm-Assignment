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
            # Check if the edge already exists
            if to_vertex in self.vertices[from_vertex]:
                print(f"Error: {from_vertex} is already following {to_vertex}.")
            else:
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

"""
# --- Test Section for Graph ---
if __name__ == "__main__":
    print("--- Testing Graph Class ---")

    g = Graph()

    print("\nAdding vertices:")
    g.addVertex("Alice")
    g.addVertex("Bob")
    g.addVertex("Charlie")
    g.addVertex("Alice") # Test adding existing vertex

    print("\nAdding edges:")
    g.addEdge("Alice", "Bob")
    g.addEdge("Alice", "Charlie")
    g.addEdge("Bob", "Charlie")
    g.addEdge("Bob", "Alice")
    g.addEdge("Charlie", "David") # Test adding edge to non-existent vertex

    print("\nListing outgoing adjacent vertices:")
    print(f"Alice's outgoing: {g.listOutgoingAdjacentVertex('Alice')}") # Expected: {'Bob', 'Charlie'}
    print(f"Bob's outgoing: {g.listOutgoingAdjacentVertex('Bob')}")     # Expected: {'Charlie', 'Alice'}
    print(f"Charlie's outgoing: {g.listOutgoingAdjacentVertex('Charlie')}") # Expected: set()
    print(f"David's outgoing: {g.listOutgoingAdjacentVertex('David')}") # Expected: Vertex not found error, set()

    print("\nRemoving edges:")
    g.removeEdge("Alice", "Bob")
    print(f"Alice's outgoing after removal: {g.listOutgoingAdjacentVertex('Alice')}") # Expected: {'Charlie'}
    g.removeEdge("Alice", "Bob") # Test removing non-existent edge

    print("\nGetting all vertices:")
    print(f"All vertices: {g.get_all_vertices()}") # Expected: ['Alice', 'Bob', 'Charlie'] (order may vary)

    print("--- Graph Class Testing Complete ---")
"""
