"""
Hospital location metadata for MediCare Multispeciality Hospital.
Contains all 18 locations across Ground Floor, First Floor, and Second Floor.
Schematic coordinates (x, y) are used strictly for 2D SVG visual rendering.
"""

LOCATIONS = {
    # --- Ground Floor (Floor 0) ---
    "G1": {
        "id": "G1",
        "name": "Main Entrance",
        "floor": 0,
        "floor_name": "Ground Floor",
        "type": "Entrance",
        "x": 80,
        "y": 300,
        "description": "Primary entry and exit point for patients and visitors."
    },
    "G2": {
        "id": "G2",
        "name": "Reception",
        "floor": 0,
        "floor_name": "Ground Floor",
        "type": "Service",
        "x": 220,
        "y": 300,
        "description": "Help desk, visitor registration, and general information."
    },
    "G3": {
        "id": "G3",
        "name": "Emergency",
        "floor": 0,
        "floor_name": "Ground Floor",
        "type": "Emergency",
        "x": 380,
        "y": 90,
        "description": "24/7 Trauma and urgent medical care unit."
    },
    "G4": {
        "id": "G4",
        "name": "Pharmacy",
        "floor": 0,
        "floor_name": "Ground Floor",
        "type": "Service",
        "x": 380,
        "y": 190,
        "description": "Dispensary for prescription medicines and health supplies."
    },
    "G5": {
        "id": "G5",
        "name": "Laboratory",
        "floor": 0,
        "floor_name": "Ground Floor",
        "type": "Diagnostic",
        "x": 380,
        "y": 290,
        "description": "Blood testing, pathology, and clinical diagnostics."
    },
    "G6": {
        "id": "G6",
        "name": "Radiology",
        "floor": 0,
        "floor_name": "Ground Floor",
        "type": "Diagnostic",
        "x": 380,
        "y": 390,
        "description": "X-Ray, CT Scan, MRI, and ultrasound imaging."
    },
    "G7": {
        "id": "G7",
        "name": "Ground Floor Stairs/Elevator",
        "floor": 0,
        "floor_name": "Ground Floor",
        "type": "Connector",
        "x": 380,
        "y": 490,
        "description": "Vertical transition to upper hospital floors."
    },

    # --- First Floor (Floor 1) ---
    "F1": {
        "id": "F1",
        "name": "Cardiology",
        "floor": 1,
        "floor_name": "First Floor",
        "type": "Department",
        "x": 380,
        "y": 90,
        "description": "Heart care, ECG, and cardiovascular treatments."
    },
    "F2": {
        "id": "F2",
        "name": "Neurology",
        "floor": 1,
        "floor_name": "First Floor",
        "type": "Department",
        "x": 380,
        "y": 190,
        "description": "Brain, nerve, and neurological disorder consultation."
    },
    "F3": {
        "id": "F3",
        "name": "Orthopedics",
        "floor": 1,
        "floor_name": "First Floor",
        "type": "Department",
        "x": 380,
        "y": 290,
        "description": "Bone fractures, joint care, and musculoskeletal clinic."
    },
    "F4": {
        "id": "F4",
        "name": "General Medicine",
        "floor": 1,
        "floor_name": "First Floor",
        "type": "Department",
        "x": 380,
        "y": 390,
        "description": "General physician consultation and routine health checks."
    },
    "F5": {
        "id": "F5",
        "name": "ENT",
        "floor": 1,
        "floor_name": "First Floor",
        "type": "Department",
        "x": 220,
        "y": 490,
        "description": "Ear, Nose, and Throat diagnostic clinic."
    },
    "F6": {
        "id": "F6",
        "name": "First Floor Stairs/Elevator",
        "floor": 1,
        "floor_name": "First Floor",
        "type": "Connector",
        "x": 380,
        "y": 490,
        "description": "Vertical transition connecting Ground Floor and Second Floor."
    },

    # --- Second Floor (Floor 2) ---
    "S1": {
        "id": "S1",
        "name": "Patient Wards",
        "floor": 2,
        "floor_name": "Second Floor",
        "type": "Patient Care",
        "x": 380,
        "y": 110,
        "description": "Inpatient rooms and recovery wards."
    },
    "S2": {
        "id": "S2",
        "name": "Pediatrics",
        "floor": 2,
        "floor_name": "Second Floor",
        "type": "Department",
        "x": 380,
        "y": 230,
        "description": "Infant, child, and adolescent healthcare clinic."
    },
    "S3": {
        "id": "S3",
        "name": "Physiotherapy",
        "floor": 2,
        "floor_name": "Second Floor",
        "type": "Department",
        "x": 380,
        "y": 350,
        "description": "Physical therapy and physical rehabilitation center."
    },
    "S4": {
        "id": "S4",
        "name": "Nursing Station",
        "floor": 2,
        "floor_name": "Second Floor",
        "type": "Service",
        "x": 220,
        "y": 490,
        "description": "Second floor administrative nursing and assistance counter."
    },
    "S5": {
        "id": "S5",
        "name": "Second Floor Stairs/Elevator",
        "floor": 2,
        "floor_name": "Second Floor",
        "type": "Connector",
        "x": 380,
        "y": 490,
        "description": "Vertical transition for Second Floor."
    }
}


def get_all_locations():
    """Return dictionary of all 18 hospital locations."""
    return LOCATIONS


def get_location_by_id(location_id):
    """
    Get location metadata by ID (case-insensitive key lookup).
    Returns location dict or None if not found.
    """
    if not location_id:
        return None
    key = str(location_id).upper().strip()
    return LOCATIONS.get(key)


def get_locations_by_floor(floor):
    """
    Get list of location metadata dicts on a specific floor (0, 1, or 2).
    """
    return [loc for loc in LOCATIONS.values() if loc["floor"] == floor]
