"""
Custom Breadth-First Search (BFS) Algorithm for Hospital Graph Navigation.
Implements an unweighted connection-based search (fewest edge hops) using a FIFO queue.
Physical distance is calculated after path discovery by summing actual graph edge weights.
"""

from collections import deque
from data.hospital_graph import get_graph, get_edge_weight
from data.locations import get_location_by_id


def bfs_search(start_id, destination_id):
    """
    Perform BFS to find a connection-based path from start_id to destination_id.

    Args:
        start_id (str): Start location ID (e.g. 'F2')
        destination_id (str): Target location ID (e.g. 'S1')

    Returns:
        dict: Path result containing node path, node names, total distance, edge count, and visited sequence.
    """
    graph = get_graph()
    start_key = str(start_id).upper().strip()
    dest_key = str(destination_id).upper().strip()

    # Validate inputs
    if start_key not in graph or dest_key not in graph:
        return {
            "success": False,
            "error": "Invalid start or destination location ID.",
            "algorithm": "BFS"
        }

    # Handle case where start == destination
    if start_key == dest_key:
        start_loc = get_location_by_id(start_key)
        return {
            "success": True,
            "algorithm": "BFS",
            "search_type": "Connection-based (Unweighted)",
            "route": [start_key],
            "route_names": [start_loc["name"] if start_loc else start_key],
            "distance": 0,
            "edge_count": 0,
            "visited_nodes": [start_key]
        }

    queue = deque([start_key])
    visited = {start_key}
    parent = {start_key: None}
    visited_sequence = []

    found = False

    while queue:
        current = queue.popleft()
        visited_sequence.append(current)

        if current == dest_key:
            found = True
            break

        # Explore neighbors ignoring edge weights (1 connection step)
        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if not found:
        return {
            "success": False,
            "error": f"No path found between {start_key} and {dest_key}.",
            "algorithm": "BFS"
        }

    # Reconstruct path from destination back to start
    path = []
    curr = dest_key
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    # Calculate actual physical distance by summing edge weights along the route
    total_distance = 0
    for i in range(len(path) - 1):
        w = get_edge_weight(path[i], path[i + 1])
        total_distance += w

    # Retrieve display names
    route_names = []
    for loc_id in path:
        loc = get_location_by_id(loc_id)
        route_names.append(loc["name"] if loc else loc_id)

    return {
        "success": True,
        "algorithm": "BFS",
        "search_type": "Connection-based (Unweighted)",
        "route": path,
        "route_names": route_names,
        "distance": total_distance,
        "edge_count": len(path) - 1,
        "visited_nodes": visited_sequence
    }
