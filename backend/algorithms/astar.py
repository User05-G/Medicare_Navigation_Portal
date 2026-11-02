"""
Custom A* Search Algorithm for Hospital Graph Navigation.
Implements a distance-aware heuristic search using f(n) = g(n) + h(n) with a min-heap priority queue.
The heuristic h(n) uses vertical floor transition lower-bounds (15m per floor) to guarantee mathematical admissibility.
"""

import heapq
from data.hospital_graph import get_graph
from data.locations import get_location_by_id


def heuristic_floor_lower_bound(node_id, destination_id):
    """
    Admissible heuristic function h(n) for hospital graph search.
    If on the same floor, h(n) = 0.
    If on different floors, h(n) = |floor(u) - floor(v)| * 15 meters.

    Args:
        node_id (str): Current node ID
        destination_id (str): Target node ID

    Returns:
        float: Admissible estimated distance lower-bound in metres.
    """
    u_loc = get_location_by_id(node_id)
    v_loc = get_location_by_id(destination_id)

    if not u_loc or not v_loc:
        return 0.0

    floor_diff = abs(u_loc["floor"] - v_loc["floor"])
    # 15 metres is the exact weight of each vertical stair/elevator connection
    return float(floor_diff * 15)


def astar_search(start_id, destination_id):
    """
    Perform custom A* search to find the shortest physical distance path from start_id to destination_id.

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
            "algorithm": "A*"
        }

    # Handle case where start == destination
    if start_key == dest_key:
        start_loc = get_location_by_id(start_key)
        return {
            "success": True,
            "algorithm": "A*",
            "search_type": "Distance-aware Heuristic Search",
            "route": [start_key],
            "route_names": [start_loc["name"] if start_loc else start_key],
            "distance": 0,
            "edge_count": 0,
            "visited_nodes": [start_key]
        }

    # Priority queue min-heap storing tuples: (f_score, counter, current_node)
    # Counter prevents comparison of node string when f_scores are tied
    counter = 0
    open_heap = []
    
    h_start = heuristic_floor_lower_bound(start_key, dest_key)
    heapq.heappush(open_heap, (h_start, counter, start_key))

    # Tracking g_score (actual cost from start to node n)
    g_score = {node: float('inf') for node in graph}
    g_score[start_key] = 0.0

    # Tracking f_score (g_score + h_score)
    f_score = {node: float('inf') for node in graph}
    f_score[start_key] = h_start

    parent = {start_key: None}
    visited_sequence = []
    open_set_items = {start_key}

    found = False

    while open_heap:
        current_f, _, current = heapq.heappop(open_heap)
        open_set_items.discard(current)

        if current not in visited_sequence:
            visited_sequence.append(current)

        if current == dest_key:
            found = True
            break

        for neighbor, weight in graph.get(current, []):
            tentative_g = g_score[current] + weight

            if tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                h_val = heuristic_floor_lower_bound(neighbor, dest_key)
                f_val = tentative_g + h_val
                f_score[neighbor] = f_val

                if neighbor not in open_set_items:
                    counter += 1
                    heapq.heappush(open_heap, (f_val, counter, neighbor))
                    open_set_items.add(neighbor)

    if not found:
        return {
            "success": False,
            "error": f"No path found between {start_key} and {dest_key}.",
            "algorithm": "A*"
        }

    # Reconstruct path from destination back to start
    path = []
    curr = dest_key
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    # Total distance is the final g_score of destination
    total_distance = int(g_score[dest_key])

    # Retrieve display names
    route_names = []
    for loc_id in path:
        loc = get_location_by_id(loc_id)
        route_names.append(loc["name"] if loc else loc_id)

    return {
        "success": True,
        "algorithm": "A*",
        "search_type": "Distance-aware Heuristic Search",
        "route": path,
        "route_names": route_names,
        "distance": total_distance,
        "edge_count": len(path) - 1,
        "visited_nodes": visited_sequence
    }
