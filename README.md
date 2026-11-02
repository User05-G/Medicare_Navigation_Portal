# MediCare Hospital Patient Navigation System

An academic AI mini-project demonstrating how **rule-based Default Reasoning** and **graph-search algorithms (BFS & A*)** work together to provide intelligent indoor navigation across a multi-floor hospital layout.

---

## 🌟 Key Architecture & Concept

The core principle of the system is a strict separation of intelligent capabilities:

> **Default Reasoning determines WHERE the user should go.**  
> **Graph Search determines HOW the user gets there.**

```text
                                USER
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Input Processing│
                         └────────┬────────┘
                                  │
                     ┌────────────┴────────────┐
                     │                         │
              Destination Given?          Requirement Given?
                     │                         │
                     │                         ▼
                     │                 ┌─────────────────┐
                     │                 │ Default Reasoning│
                     │                 └────────┬────────┘
                     │                          │
                     └────────────┬─────────────┘
                                  ▼
                        ┌─────────────────────┐
                        │ Destination Confirmed│
                        └──────────┬──────────┘
                                   ▼
                         ┌──────────────────┐
                         │  Hospital Graph  │
                         └────────┬─────────┘
                                  ▼
                        ┌────────────────────┐
                        │ Select Search      │
                        │ BFS / A*           │
                        └─────────┬──────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Route Processing │
                         └────────┬─────────┘
                                  ▼
                     ┌──────────────────────────┐
                     │ Distance + Floor + Time  │
                     └────────────┬─────────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Navigation Result│
                         └────────┬─────────┘
                                  ▼
                         ┌──────────────────┐
                         │ React SVG Map    │
                         └──────────────────┘
```

---

## ✨ Features

- **Rule-Based Default Reasoning**: Interprets natural language requirements (e.g., *"I need a blood test"*) to map patients to hospital departments (*Laboratory*) using case-insensitive keyword rules.
- **Custom Breadth-First Search (BFS)**: Unweighted connection-based search finding the route with the minimum number of edge transitions.
- **Custom A* Search**: Distance-aware heuristic search using $f(n) = g(n) + h(n)$ with a mathematically admissible floor-transition lower bound $h(u, v) = |floor_u - floor_v| \times 15\text{m}$.
- **Interactive 2D Schematic SVG Map**: Features 3 floor switcher tabs (Ground Floor, 1st Floor, 2nd Floor), node placement, corridor lines, glowing cyan route polylines, start (🟢) and destination (🔴) markers, and map legend.
- **Side-by-Side Algorithm Comparison**: `/api/compare` endpoint and UI matrix comparing BFS vs A* route, distance, step count, and execution time.
- **Walking Time Estimator**: Calculates estimated walking time based on a $1.2\text{ m/s}$ average walking speed.
- **Automated Test Suite**: 17 Pytest unit tests covering reasoning rules, BFS pathing, A* pathing, $75\text{m}$ Neurology $\rightarrow$ Patient Wards verification, heuristic admissibility across all pairs, and Flask REST endpoints.

---

## 🏥 Hospital Layout & Graph Representation

**MediCare Multispeciality Hospital** consists of **18 locations** across 3 floors and **17 bidirectional connections**:

### Locations (18)

| Floor | ID | Location Name | Type |
|---|---|---|---|
| **Ground Floor** | G1 | Main Entrance | Entrance |
| | G2 | Reception | Service |
| | G3 | Emergency | Emergency |
| | G4 | Pharmacy | Service |
| | G5 | Laboratory | Diagnostic |
| | G6 | Radiology | Diagnostic |
| | G7 | Ground Floor Stairs/Elevator | Connector |
| **First Floor** | F1 | Cardiology | Department |
| | F2 | Neurology | Department |
| | F3 | Orthopedics | Department |
| | F4 | General Medicine | Department |
| | F5 | ENT | Department |
| | F6 | First Floor Stairs/Elevator | Connector |
| **Second Floor** | S1 | Patient Wards | Patient Care |
| | S2 | Pediatrics | Department |
| | S3 | Physiotherapy | Department |
| | S4 | Nursing Station | Service |
| | S5 | Second Floor Stairs/Elevator | Connector |

### Bidirectional Graph Connections (17)

- **Ground Floor (6 connections)**:
  `G1 ↔ G2 (10m)`, `G2 ↔ G3 (15m)`, `G2 ↔ G4 (20m)`, `G2 ↔ G5 (25m)`, `G2 ↔ G6 (30m)`, `G2 ↔ G7 (15m)`
- **Vertical Connectors (2 connections)**:
  `G7 ↔ F6 (15m)`, `F6 ↔ S5 (15m)`
- **First Floor (5 connections)**:
  `F6 ↔ F1 (25m)`, `F6 ↔ F2 (35m)`, `F6 ↔ F3 (30m)`, `F6 ↔ F4 (30m)`, `F6 ↔ F5 (40m)`
- **Second Floor (4 connections)**:
  `S5 ↔ S1 (25m)`, `S5 ↔ S2 (30m)`, `S5 ↔ S3 (35m)`, `S5 ↔ S4 (20m)`

---

## 🧠 Rule-Based Reasoning Mappings

| Requirement / Keyword | Target Department | ID | Floor |
|---|---|---|---|
| `chest pain`, `heart problem` | Cardiology | F1 | First Floor |
| `broken bone`, `fracture`, `bone injury` | Orthopedics | F3 | First Floor |
| `head problem`, `headache`, `neurological` | Neurology | F2 | First Floor |
| `ear problem`, `ear` | ENT | F5 | First Floor |
| `blood test`, `blood examination` | Laboratory | G5 | Ground Floor |
| `x-ray`, `scan`, `imaging` | Radiology | G6 | Ground Floor |
| `medicine`, `prescription medicine` | Pharmacy | G4 | Ground Floor |
| `child`, `child treatment` | Pediatrics | S2 | Second Floor |
| `physical therapy`, `rehabilitation` | Physiotherapy | S3 | Second Floor |
| `emergency` | Emergency | G3 | Ground Floor |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Flask 3.0.3, Flask-CORS 4.0.1, Pytest 8.2.2
- **Frontend**: React 19, Vite 8.3, Vanilla CSS3, SVG
- **Algorithms**: Custom Python Queue-based BFS and Priority-Queue Min-Heap A* (No NetworkX or external graph search libraries used).

---

## 📂 Repository Directory Structure

```text
Medicare_Navigation_Portal/
│
├── backend/
│   ├── app.py                      # Flask REST API Server
│   ├── requirements.txt            # Python Dependencies
│   │
│   ├── data/
│   │   ├── locations.py            # 18 Location metadata with schematic (x,y)
│   │   ├── hospital_graph.py       # Adjacency list with 17 weighted edges
│   │   └── reasoning_rules.py      # Case-insensitive phrase-to-department rules
│   │
│   ├── reasoning/
│   │   └── rules.py                # Requirement matching engine & flow steps
│   │
│   ├── algorithms/
│   │   ├── bfs.py                  # Custom connection-based unweighted BFS
│   │   └── astar.py                # Custom distance-aware A* search
│   │
│   ├── services/
│   │   └── navigation_service.py   # Route calculation, walking time & comparison
│   │
│   └── tests/
│       └── test_navigation.py      # Pytest test suite (17 passing tests)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Navigation header & tab switcher
│   │   │   ├── NavigationForm.jsx  # Control panel (Direct & Intelligent modes)
│   │   │   ├── ReasoningResult.jsx # Transparent reasoning flow visualization
│   │   │   ├── NavigationResult.jsx# Route summary metrics & timeline
│   │   │   ├── HospitalMap.jsx     # Interactive 2D SVG map & Legend
│   │   │   ├── AlgorithmComparison.jsx # Side-by-side BFS vs A* comparison
│   │   │   ├── HowItWorks.jsx      # Architecture breakdown (01-03)
│   │   │   └── About.jsx           # Project metadata & disclaimers
│   │   │
│   │   ├── services/
│   │   │   └── api.js              # Fetch client wrapper for Flask API
│   │   │
│   │   ├── App.jsx                 # Main React container
│   │   ├── main.jsx                # Entry point
│   │   └── index.css               # Modern healthcare CSS design system
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md                       # Project documentation
```

---

## ⚡ Setup & Run Instructions

### 1. Backend (Flask)

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt

# Run Flask server (starts on http://127.0.0.1:5000)
python app.py
```

### 2. Run Backend Tests

```bash
cd backend
pytest tests/test_navigation.py -v
```

### 3. Frontend (React + Vite)

```bash
# Navigate to frontend directory
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server (starts on http://localhost:5173)
npm run dev
```

---

## 🌐 API Endpoints

- `GET /api/locations`: List all 18 hospital locations grouped by floor.
- `POST /api/reason`: Submit requirement prompt (`{ "query": "I need a blood test" }`).
- `POST /api/navigate`: Calculate direct route (`{ "start": "F2", "destination": "S1", "algorithm": "astar" }`).
- `POST /api/intelligent-navigate`: Calculate intelligent route (`{ "start": "G1", "query": "I have a broken leg", "algorithm": "astar" }`).
- `POST /api/compare`: Compare BFS vs A* side-by-side (`{ "start": "F2", "destination": "S1" }`).

---

## ⚠️ Academic Disclaimers

1. The hospital graph, locations, and distances are simulated values for academic demonstration.
2. The Default Reasoning system performs phrase matching to identify hospital service departments and does **NOT** provide medical diagnosis.
3. No database, external machine learning libraries, or third-party AI APIs are used.
