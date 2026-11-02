"""
Rule-Based Default Reasoning Engine for Hospital Navigation.
Maps natural language user requirements to predefined hospital destinations without machine learning or external APIs.
"""

from data.reasoning_rules import REASONING_RULES
from data.locations import get_location_by_id


def evaluate_requirement(user_query):
    """
    Evaluate user requirement using case-insensitive phrase/keyword matching.

    Args:
        user_query (str): Natural language prompt entered by user.

    Returns:
        dict: Result containing success status, identified destination, matched rule, and reasoning steps.
    """
    if not user_query or not isinstance(user_query, str):
        return {
            "success": False,
            "query": user_query or "",
            "matched_keyword": None,
            "destination_id": None,
            "destination_name": None,
            "reason": "Please provide a valid requirement description.",
            "flow_steps": []
        }

    normalized_query = user_query.lower().strip()

    # Search for matching keywords in rules
    for rule in REASONING_RULES:
        for keyword in rule["keywords"]:
            if keyword.lower() in normalized_query:
                dest_id = rule["department_id"]
                dest_name = rule["department_name"]
                loc_meta = get_location_by_id(dest_id)
                floor_name = loc_meta["floor_name"] if loc_meta else ""

                flow_steps = [
                    f"User Requirement: '{user_query}'",
                    f"Matched Rule Keyword: '{keyword}' → {dest_name}",
                    f"Identified Destination: {dest_name} ({floor_name})"
                ]

                return {
                    "success": True,
                    "query": user_query,
                    "matched_keyword": keyword,
                    "destination_id": dest_id,
                    "destination_name": dest_name,
                    "destination_floor": loc_meta["floor"] if loc_meta else 0,
                    "destination_floor_name": floor_name,
                    "reason": f"Requirement matches keyword '{keyword}' which maps to the {dest_name} department.",
                    "explanation": rule["explanation"],
                    "flow_steps": flow_steps
                }

    # Fallback when no rule matches
    return {
        "success": False,
        "query": user_query,
        "matched_keyword": None,
        "destination_id": None,
        "destination_name": None,
        "destination_floor": None,
        "destination_floor_name": None,
        "reason": "I couldn't identify a destination from that requirement. Please select a destination manually.",
        "explanation": "No predefined rule keyword matched the provided text.",
        "flow_steps": [
            f"User Requirement: '{user_query}'",
            "Rule Matching: No matching keywords found in rule-based dictionary.",
            "Destination: Unidentified (Manual selection required)."
        ]
    }
