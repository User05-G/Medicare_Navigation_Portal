"""
Predefined default reasoning rules mapping patient keywords/phrases to hospital department destinations.
Note: This is pure rule-based requirement mapping for indoor navigation and NOT medical diagnosis.
"""

REASONING_RULES = [
    {
        "department_id": "F1",
        "department_name": "Cardiology",
        "keywords": ["chest pain", "heart problem", "heart pain", "cardiac", "chest pressure"],
        "explanation": "Requirement indicates cardiovascular or heart-related consultation."
    },
    {
        "department_id": "F3",
        "department_name": "Orthopedics",
        "keywords": ["broken bone", "fracture", "bone injury", "broken leg", "broken arm", "joint pain", "sprain"],
        "explanation": "Requirement indicates bone, joint, or fracture evaluation."
    },
    {
        "department_id": "F2",
        "department_name": "Neurology",
        "keywords": ["head problem", "headache", "neurological problem", "migraine", "dizziness", "seizure"],
        "explanation": "Requirement indicates brain, nerve, or neurological consultation."
    },
    {
        "department_id": "F5",
        "department_name": "ENT",
        "keywords": ["ear problem", "ear", "ear pain", "hearing problem", "nose problem", "throat pain"],
        "explanation": "Requirement indicates Ear, Nose, or Throat specialist consultation."
    },
    {
        "department_id": "G5",
        "department_name": "Laboratory",
        "keywords": ["blood test", "blood examination", "blood work", "lab test", "urine test", "blood sample"],
        "explanation": "Requirement indicates pathology, blood sample, or lab diagnostic services."
    },
    {
        "department_id": "G6",
        "department_name": "Radiology",
        "keywords": ["x-ray", "x ray", "scan", "imaging", "mri", "ct scan", "ultrasound"],
        "explanation": "Requirement indicates medical imaging or diagnostic radiological scan."
    },
    {
        "department_id": "G4",
        "department_name": "Pharmacy",
        "keywords": ["medicine", "prescription medicine", "pills", "medication", "buy medicine", "chemist"],
        "explanation": "Requirement indicates pharmaceutical dispensation or prescription medicine pickup."
    },
    {
        "department_id": "S2",
        "department_name": "Pediatrics",
        "keywords": ["child", "child treatment", "pediatrician", "baby checkup", "infant care", "kid health"],
        "explanation": "Requirement indicates pediatric or child medical treatment."
    },
    {
        "department_id": "S3",
        "department_name": "Physiotherapy",
        "keywords": ["physical therapy", "rehabilitation", "physio", "muscle rehab", "exercise therapy"],
        "explanation": "Requirement indicates physical therapy or physical rehabilitation."
    },
    {
        "department_id": "G3",
        "department_name": "Emergency",
        "keywords": ["emergency", "urgent care", "trauma", "severe injury", "accident"],
        "explanation": "Requirement indicates urgent emergency medical attention."
    }
]


def get_reasoning_rules():
    """Get all predefined reasoning rules."""
    return REASONING_RULES
