"""
Flask REST API server for MediCare Hospital Patient Navigation System.
Exposes REST endpoints for hospital locations, default reasoning, direct navigation, intelligent navigation, and algorithm comparison.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from data.locations import get_all_locations, get_location_by_id, LOCATIONS
from reasoning.rules import evaluate_requirement
from services.navigation_service import (
    execute_route_planning,
    execute_intelligent_navigation,
    compare_algorithms
)

app = Flask(__name__)
# Enable CORS for local React development
CORS(app)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Server health status endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "MediCare Hospital Patient Navigation System Backend",
        "version": "1.0.0"
    }), 200


@app.route("/api/locations", methods=["GET"])
def list_locations():
    """
    Get all 18 hospital locations grouped by floor.
    """
    all_locs = get_all_locations()

    ground_floor = [loc for loc in all_locs.values() if loc["floor"] == 0]
    first_floor = [loc for loc in all_locs.values() if loc["floor"] == 1]
    second_floor = [loc for loc in all_locs.values() if loc["floor"] == 2]

    return jsonify({
        "success": True,
        "total": len(all_locs),
        "locations": list(all_locs.values()),
        "by_floor": {
            "ground": ground_floor,
            "first": first_floor,
            "second": second_floor
        }
    }), 200


@app.route("/api/reason", methods=["POST"])
def default_reasoning_endpoint():
    """
    Endpoint for Default Reasoning requirement identification.
    Expected JSON Payload: { "query": "I need a blood test" }
    """
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({
            "success": False,
            "error": "Query field is required and cannot be empty."
        }), 400

    res = evaluate_requirement(query)
    status_code = 200 if res["success"] else 404
    return jsonify(res), status_code


@app.route("/api/navigate", methods=["POST"])
def direct_navigate_endpoint():
    """
    Endpoint for Direct Navigation.
    Expected JSON Payload: { "start": "G1", "destination": "G5", "algorithm": "astar" }
    """
    data = request.get_json(silent=True) or {}

    start_id = str(data.get("start", "")).upper().strip()
    destination_id = str(data.get("destination", "")).upper().strip()
    algorithm = str(data.get("algorithm", "astar")).lower().strip()

    if not start_id or not destination_id:
        return jsonify({
            "success": False,
            "error": "Both 'start' and 'destination' location IDs are required."
        }), 400

    if not get_location_by_id(start_id):
        return jsonify({
            "success": False,
            "error": f"Invalid start location ID: '{start_id}'."
        }), 400

    if not get_location_by_id(destination_id):
        return jsonify({
            "success": False,
            "error": f"Invalid destination location ID: '{destination_id}'."
        }), 400

    if algorithm not in ["bfs", "astar"]:
        return jsonify({
            "success": False,
            "error": f"Unsupported algorithm '{algorithm}'. Must be 'bfs' or 'astar'."
        }), 400

    if start_id == destination_id:
        loc = get_location_by_id(start_id)
        return jsonify({
            "success": True,
            "mode": "Direct Navigation",
            "start": loc,
            "destination": loc,
            "algorithm": algorithm.upper(),
            "route": [start_id],
            "route_names": [loc["name"]],
            "route_steps": [{
                "step_index": 1,
                "id": loc["id"],
                "name": loc["name"],
                "floor": loc["floor"],
                "floor_name": loc["floor_name"],
                "type": loc["type"],
                "is_connector": False
            }],
            "distance": 0,
            "estimated_time": "0 sec",
            "estimated_seconds": 0,
            "edge_count": 0,
            "floors_traversed": [loc["floor"]],
            "destination_floor": loc["floor"],
            "message": "You are already at the selected destination."
        }), 200

    result = execute_route_planning(start_id, destination_id, algorithm)
    return jsonify(result), 200


@app.route("/api/intelligent-navigate", methods=["POST"])
def intelligent_navigate_endpoint():
    """
    Endpoint for Intelligent Navigation: Requirement Prompt -> Default Reasoning -> Route.
    Expected JSON Payload: { "start": "G1", "query": "I have a broken leg", "algorithm": "astar" }
    """
    data = request.get_json(silent=True) or {}

    start_id = str(data.get("start", "")).upper().strip()
    query = str(data.get("query", "")).strip()
    algorithm = str(data.get("algorithm", "astar")).lower().strip()

    if not start_id or not query:
        return jsonify({
            "success": False,
            "error": "Both 'start' location ID and 'query' text are required."
        }), 400

    if not get_location_by_id(start_id):
        return jsonify({
            "success": False,
            "error": f"Invalid start location ID: '{start_id}'."
        }), 400

    if algorithm not in ["bfs", "astar"]:
        return jsonify({
            "success": False,
            "error": f"Unsupported algorithm '{algorithm}'. Must be 'bfs' or 'astar'."
        }), 400

    result = execute_intelligent_navigation(start_id, query, algorithm)
    status_code = 200 if result.get("success") else 422
    return jsonify(result), status_code


@app.route("/api/compare", methods=["POST"])
def compare_algorithms_endpoint():
    """
    Endpoint for comparing BFS vs A* side-by-side.
    Expected JSON Payload: { "start": "F2", "destination": "S1" }
    """
    data = request.get_json(silent=True) or {}

    start_id = str(data.get("start", "")).upper().strip()
    destination_id = str(data.get("destination", "")).upper().strip()

    if not start_id or not destination_id:
        return jsonify({
            "success": False,
            "error": "Both 'start' and 'destination' location IDs are required."
        }), 400

    if not get_location_by_id(start_id) or not get_location_by_id(destination_id):
        return jsonify({
            "success": False,
            "error": "One or both location IDs are invalid."
        }), 400

    result = compare_algorithms(start_id, destination_id)
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
