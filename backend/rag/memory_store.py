import json
import os
from typing import List, Dict


MEMORY_PATH = "backend/rag/memory.json"


class MemoryStore:
    def __init__(self):
        os.makedirs("backend/rag", exist_ok=True)
        if not os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, "w") as f:
                json.dump([], f)

    def read(self) -> List[Dict]:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, entries: List[Dict]):
        existing = self.read()
        existing.extend(entries)

        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

    def summarize_failures(self) -> List[str]:
        memory = self.read()
        insights = []

        for m in memory:
            if m.get("verdict") != "pass":
                insights.append(m["description"])

        return list(set(insights))
