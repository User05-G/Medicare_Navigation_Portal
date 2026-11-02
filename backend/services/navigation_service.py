"""
Navigation Service module orchestrating reasoning, route planning, estimated walking time calculation, floor breakdown, and side-by-side algorithm comparison.
"""

import time
from data.locations import get_location_by_id
from reasoning.rules import evaluate_requirement
from algorithms.bfs import bfs_search
from algorithms.astar import astar_search

# Configurable average walking speed in metres per second (1.2 m/s ~ 4.3 km/h)
WALKING_SPEED_MPS = 1.2


def calculate_walking_time(distance_meters):
    """
    Calculate estimated walking time from physical route distance.

    Args:
        distance_meters (int/float): Route physical distance in metres.

    Returns:
        dict: Formatted time metadata (seconds, formatted string).
    """
    if distance_meters <= 0:
        return {"seconds": 0, "formatted": "0 sec"}

    seconds = round(distance_meters / WALKING_SPEED_MPS)

    if seconds < 60:
        formatted = f"{seconds} sec"
    else:
        minutes = round(seconds / 60)
        formatted = f"~{minutes} min" if minutes > 1 else "~1 min"

    return {
        "seconds": seconds,
        "formatted": formatted
    }


def format_route_details(route_ids):
    """
    Build rich step-by-step route details including node metadata and floor transitions.

    Args:
        route_ids (list): List of location ID strings.

    Returns:
        list: Detailed list of node dictionaries with step indexes and connector flags.
    """
    steps = []
    for idx, loc_id in enumerate(route_ids):
        loc = get_location_by_id(loc_id)
        if loc:
            steps.append({
                "step_index": idx + 1,
                "id": loc["id"],
                "name": loc["name"],
                "floor": loc["floor"],
                "floor_name": loc["floor_name"],
                "type": loc["type"],
                "is_connector": loc["type"] == "Connector"
            })
        else:
            steps.append({
                "step_index": idx + 1,
                "id": loc_id,
                "name": loc_id,
                "floor": 0,
                "floor_name": "Ground Floor",
                "type": "Unknown",
                "is_connector": False
            })
    return steps


def get_floors_involved(route_ids):
    """
    Extract set of unique floor indices traversed in the route.

    Args:
        route_ids (list): List of location IDs.

    Returns:
        list: Sorted list of integer floor indices (e.g. [1, 2]).
    """
    floors = set()
    for loc_id in route_ids:
        loc = get_location_by_id(loc_id)
        if loc:
            floors.add(loc["floor"])
    return sorted(list(floors))


def execute_route_planning(start_id, destination_id, algorithm="astar"):
    """
    Execute route planning using selected algorithm (BFS or A*).

    Args:
        start_id (str): Start location ID
        destination_id (str): Destination location ID
        algorithm (str): 'bfs' or 'astar'

    Returns:
        dict: Navigation result payload.
    """
    algo_key = str(algorithm).lower().strip()

    t_start = time.perf_counter()
    if algo_key == "bfs":
        res = bfs_search(start_id, destination_id)
    else:
        res = astar_search(start_id, destination_id)
    t_end = time.perf_counter()

    execution_time_ms = round((t_end - t_start) * 1000, 3)

    if not res.get("success"):
        return res

    route_ids = res["route"]
    distance = res["distance"]
    time_info = calculate_walking_time(distance)
    steps_detailed = format_route_details(route_ids)
    floors_traversed = get_floors_involved(route_ids)

    start_loc = get_location_by_id(start_id)
    dest_loc = get_location_by_id(destination_id)

    return {
        "success": True,
        "mode": "Direct Navigation",
        "start": {
            "id": start_loc["id"] if start_loc else start_id,
            "name": start_loc["name"] if start_loc else start_id,
            "floor": start_loc["floor"] if start_loc else 0,
            "floor_name": start_loc["floor_name"] if start_loc else ""
        },
        "destination": {
            "id": dest_loc["id"] if dest_loc else destination_id,
            "name": dest_loc["name"] if dest_loc else destination_id,
            "floor": dest_loc["floor"] if dest_loc else 0,
            "floor_name": dest_loc["floor_name"] if dest_loc else ""
        },
        "algorithm": res["algorithm"],
        "search_type": res["search_type"],
        "route": route_ids,
        "route_names": res["route_names"],
        "route_steps": steps_detailed,
        "distance": distance,
        "estimated_time": time_info["formatted"],
        "estimated_seconds": time_info["seconds"],
        "edge_count": res["edge_count"],
        "floors_traversed": floors_traversed,
        "destination_floor": dest_loc["floor"] if dest_loc else 0,
        "execution_time_ms": execution_time_ms,
        "visited_nodes": res.get("visited_nodes", [])
    }


def execute_intelligent_navigation(start_id, user_query, algorithm="astar"):
    """
    Execute intelligent navigation: Default Reasoning -> Destination -> Graph Search.

    Args:
        start_id (str): Start location ID
        user_query (str): Patient requirement prompt (e.g. 'I need a blood test')
        algorithm (str): 'bfs' or 'astar'

    Returns:
        dict: Combined reasoning and navigation result.
    """
    # Step 1: Default Reasoning
    reasoning_res = evaluate_requirement(user_query)

    if not reasoning_res.get("success"):
        return {
            "success": False,
            "mode": "Intelligent Navigation",
            "reasoning": reasoning_res,
            "error": reasoning_res.get("reason")
        }

    destination_id = reasoning_res["destination_id"]

    # Step 2: Route Planning
    nav_res = execute_route_planning(start_id, destination_id, algorithm)

    if not nav_res.get("success"):
        return nav_res

    nav_res["mode"] = "Intelligent Navigation"
    nav_res["reasoning"] = reasoning_res

    return nav_res


def compare_algorithms(start_id, destination_id):
    """
    Run both BFS and A* on the same query to provide side-by-side metrics.

    Args:
        start_id (str): Start location ID
        destination_id (str): Destination location ID

    Returns:
        dict: Comparative summary object.
    """
    bfs_res = execute_route_planning(start_id, destination_id, algorithm="bfs")
    astar_res = execute_route_planning(start_id, destination_id, algorithm="astar")

    return {
        "success": True,
        "start_id": start_id,
        "destination_id": destination_id,
        "bfs": bfs_res,
        "astar": astar_res,
        "comparison": {
            "same_route": bfs_res.get("route") == astar_res.get("route"),
            "distance_diff": abs(bfs_res.get("distance", 0) - astar_res.get("distance", 0)),
            "bfs_description": "Connection-based exploration (minimizes edge count).",
            "astar_description": "Distance-aware heuristic search (minimizes physical distance in metres)."
        }
    }
