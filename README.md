# Multi-Agent Game Tester POC

## Overview
This project is a Proof of Concept (POC) for an AI-powered **multi-agent game testing system** designed to automatically test web-based number/math puzzle games.

The system uses a **multi-agent architecture** to:
- Generate intelligent test cases
- Rank and select high-impact tests
- Execute tests in a real browser
- Capture execution artifacts
- Validate results using repeat and cross-run checks
- Learn over time using RAG-based memory

Target example game: https://play.ezygamers.com/  
However, the system is **game-agnostic** and works with any similar web-based puzzle or math game.

---

## Key Features

### 🧠 Multi-Agent Architecture
- **PlannerAgent** – Generates 20+ candidate test cases
- **RankerAgent** – Prioritizes test cases and selects top 10
- **ExecutorAgent** – Executes tests using Playwright in a real browser
- **AnalyzerAgent** – Performs repeat and cross-run validation
- **OrchestratorAgent** – Coordinates the entire workflow

---

### 🌐 Real Browser Testing
- Uses **Playwright (Async API)**
- Opens the game URL automatically
- Performs safe interactions
- Works without hardcoding game logic

---

### 📸 Artifact Collection
For every test execution, the system captures:
- Before & after screenshots
- DOM snapshot
- Browser console logs

Artifacts are saved under: backend/artifacts/


---

### 🔁 Repeat & Cross-Run Validation
Each test is executed **multiple times** to detect:
- Flaky behavior
- Inconsistent UI or logic

Validation is done by comparing visual artifacts (hash-based).

---

### 🧠 Learning with RAG (Retrieval-Augmented Generation)
- Past test results are stored in persistent memory
- Planner retrieves historical issues
- Future test plans improve automatically over time

Memory storage: backend/rag/memory.json

---

### 📄 Persistent Reports
Every execution produces a timestamped JSON report containing:
- Test verdicts
- Stability analysis
- Artifact references

Saved under: backend/reports/

---

## Project Structure
```bash
multi-agent-game-tester/
│
├── backend/
│ ├── main.py
│ ├── agents/
│ │ ├── planner.py
│ │ ├── ranker.py
│ │ ├── executor.py
│ │ ├── analyzer.py
│ │ └── orchestrator.py
│ ├── rag/
│ │ ├── memory_store.py
│ │ └── memory.json
│ ├── artifacts/
│ └── reports/
│
├── frontend/
│ └── index.html (optional minimal UI)
│
├── requirements.txt
├── README.md
└── demo_video.mp4
```

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone <your-github-repo-url>
cd multi-agent-game-tester
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### Running the Application
```bash
uvicorn backend.main:app --port 8001
```

### Open API docs:
```bash
http://127.0.0.1:8001/docs
```

### Usage
#### Generate Test Plan
**POST /plan**
```bash
{
  "url": "https://play.ezygamers.com/"
}
```

#### Execute Tests
**POST /execute**
```bash
{
  "url": "https://play.ezygamers.com/"
}
```

## Output

- Execution artifacts → backend/artifacts/
- Final JSON report → backend/reports/
- Learning memory → backend/rag/memory.json

## Notes

This project is intentionally designed as a POC focusing on:
- Architecture clarity
- Agent-based reasoning
- Reproducible evidence
- Extensibility

It can be extended with:
- Smarter LLM-driven interactions
- Game-specific solvers
- Distributed execution