"""
Comprehensive Pytest Test Suite for MediCare Hospital Patient Navigation System.
Verifies Default Reasoning, BFS unweighted pathing, A* weighted pathing, distance calculation,
admissibility of A* heuristic across all node pairs, and Flask REST API endpoints.
"""

import pytest
import sys
import os

# Add backend directory to sys.path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from data.locations import LOCATIONS, get_location_by_id
from data.hospital_graph import get_graph, get_edge_weight
from reasoning.rules import evaluate_requirement
from algorithms.bfs import bfs_search
from algorithms.astar import astar_search, heuristic_floor_lower_bound
from services.navigation_service import execute_route_planning, execute_intelligent_navigation


# --- 1. DEFAULT REASONING TESTS ---

def test_reasoning_cardiology():
    res = evaluate_requirement("chest pain")
    assert res["success"] is True
    assert res["destination_id"] == "F1"
    assert res["destination_name"] == "Cardiology"


def test_reasoning_orthopedics():
    res = evaluate_requirement("I have a broken leg")
    assert res["success"] is True
    assert res["destination_id"] == "F3"
    assert res["destination_name"] == "Orthopedics"


def test_reasoning_laboratory():
    res = evaluate_requirement("I need a blood test")
    assert res["success"] is True
    assert res["destination_id"] == "G5"
    assert res["destination_name"] == "Laboratory"


def test_reasoning_pharmacy():
    res = evaluate_requirement("I need medicine")
    assert res["success"] is True
    assert res["destination_id"] == "G4"
    assert res["destination_name"] == "Pharmacy"


def test_reasoning_ent():
    res = evaluate_requirement("I have an ear problem")
    assert res["success"] is True
    assert res["destination_id"] == "F5"
    assert res["destination_name"] == "ENT"


def test_reasoning_emergency():
    res = evaluate_requirement("emergency")
    assert res["success"] is True
    assert res["destination_id"] == "G3"
    assert res["destination_name"] == "Emergency"


def test_reasoning_unmapped_fallback():
    res = evaluate_requirement("I need something that is not represented by the rules")
    assert res["success"] is False
    assert res["destination_id"] is None
    assert "couldn't identify" in res["reason"].lower()


# --- 2. SEARCH ALGORITHM & DISTANCE TESTS ---

def test_bfs_direct_test1():
    """Test 1: G1 (Main Entrance) -> G2 (Reception) via BFS."""
    res = bfs_search("G1", "G2")
    assert res["success"] is True
    assert res["route"] == ["G1", "G2"]
    assert res["distance"] == 10
    assert res["edge_count"] == 1


def test_astar_neurology_to_patient_wards_test2():
    """Test 2: F2 (Neurology) -> S1 (Patient Wards) via A*."""
    res = astar_search("F2", "S1")
    assert res["success"] is True
    assert res["route"] == ["F2", "F6", "S5", "S1"]
    # 35 (F2->F6) + 15 (F6->S5) + 25 (S5->S1) = 75m
    assert res["distance"] == 75
    assert res["edge_count"] == 3


def test_intelligent_navigation_test3():
    """Test 3: Start: G1 (Main Entrance), Query: 'I need a blood test', Algorithm: A*."""
    res = execute_intelligent_navigation("G1", "I need a blood test", algorithm="astar")
    assert res["success"] is True
    assert res["reasoning"]["destination_id"] == "G5"
    # G1 -> G2 (10) + G2 -> G5 (25) = 35m
    assert res["route"] == ["G1", "G2", "G5"]
    assert res["distance"] == 35


def test_intelligent_navigation_test4():
    """Test 4: Start: F1 (Cardiology), Query: 'I need medicine', Algorithm: BFS."""
    res = execute_intelligent_navigation("F1", "I need medicine", algorithm="bfs")
    assert res["success"] is True
    assert res["reasoning"]["destination_id"] == "G4"
    # F1 -> F6 (25) + F6 -> G7 (15) + G7 -> G2 (15) + G2 -> G4 (20) = 75m
    assert res["route"] == ["F1", "F6", "G7", "G2", "G4"]
    assert res["distance"] == 75


# --- 3. HEURISTIC ADMISSIBILITY TEST ---

def test_heuristic_admissibility_across_all_pairs():
    """
    Verify that h(u, v) <= actual_shortest_path_distance(u, v) for all 18x18 node pairs in the graph.
    This guarantees that the floor-transition heuristic is mathematically admissible.
    """
    all_nodes = list(LOCATIONS.keys())
    for u in all_nodes:
        for v in all_nodes:
            h_val = heuristic_floor_lower_bound(u, v)
            shortest_res = astar_search(u, v)
            assert shortest_res["success"] is True
            actual_dist = shortest_res["distance"]
            assert h_val <= actual_dist, f"Heuristic overestimation for pair ({u}, {v}): h={h_val} > actual={actual_dist}"


# --- 4. FLASK API REST ENDPOINTS TESTS ---

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_api_locations(client):
    response = client.get('/api/locations')
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["total"] == 18
    assert len(data["by_floor"]["ground"]) == 7
    assert len(data["by_floor"]["first"]) == 6
    assert len(data["by_floor"]["second"]) == 5


def test_api_navigate(client):
    response = client.post('/api/navigate', json={
        "start": "F2",
        "destination": "S1",
        "algorithm": "astar"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["distance"] == 75
    assert data["route"] == ["F2", "F6", "S5", "S1"]


def test_api_intelligent_navigate(client):
    response = client.post('/api/intelligent-navigate', json={
        "start": "G1",
        "query": "I have a broken leg",
        "algorithm": "astar"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["reasoning"]["destination_id"] == "F3"


def test_api_compare(client):
    response = client.post('/api/compare', json={
        "start": "F2",
        "destination": "S1"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "bfs" in data
    assert "astar" in data
