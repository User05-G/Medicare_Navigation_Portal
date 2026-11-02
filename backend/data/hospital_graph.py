"""
Hospital graph structure for MediCare Multispeciality Hospital.
Represented as an Adjacency List containing all 18 nodes and 17 bidirectional edges with physical distances in metres.
"""

# Base list of 17 undirected weighted edges (u, v, distance_meters)
EDGES = [
    # Ground Floor Connections (6)
    ("G1", "G2", 10),
    ("G2", "G3", 15),
    ("G2", "G4", 20),
    ("G2", "G5", 25),
    ("G2", "G6", 30),
    ("G2", "G7", 15),

    # Vertical Connectors (2)
    ("G7", "F6", 15),
    ("F6", "S5", 15),

    # First Floor Connections (5)
    ("F6", "F1", 25),
    ("F6", "F2", 35),
    ("F6", "F3", 30),
    ("F6", "F4", 30),
    ("F6", "F5", 40),

    # Second Floor Connections (4)
    ("S5", "S1", 25),
    ("S5", "S2", 30),
    ("S5", "S3", 35),
    ("S5", "S4", 20)
]


def build_hospital_graph():
    """
    Constructs and returns the bidirectional adjacency list dictionary.
    Structure:
    {
        "G1": [("G2", 10)],
        "G2": [("G1", 10), ("G3", 15), ("G4", 20), ("G5", 25), ("G6", 30), ("G7", 15)],
        ...
    }
    """
    graph = {}

    for u, v, weight in EDGES:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []

        # Add bidirectional connections
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    return graph


# Singleton instance of the graph
HOSPITAL_GRAPH = build_hospital_graph()


def get_graph():
    """Get the hospital adjacency list representation."""
    return HOSPITAL_GRAPH


def get_neighbors(node_id):
    """
    Get list of neighbor tuples (neighbor_id, edge_weight) for a given node.
    """
    node_key = str(node_id).upper().strip()
    return HOSPITAL_GRAPH.get(node_key, [])


def get_edge_weight(u, v):
    """
    Get physical edge weight in meters between adjacent nodes u and v.
    Returns weight or float('inf') if not directly connected.
    """
    u_key = str(u).upper().strip()
    v_key = str(v).upper().strip()

    for neighbor, weight in HOSPITAL_GRAPH.get(u_key, []):
        if neighbor == v_key:
            return weight

    return float('inf')
