from backend.rag.memory_store import MemoryStore

import uuid
from typing import List, Dict

class PlannerAgent:
    """
    Generates candidate test cases using RAG memory
    """

    def __init__(self):
        self.memory = MemoryStore()

    def generate_test_cases(self, game_url: str):
        test_cases = []

        base_tests = [
            "Start game and verify it loads",
            "Submit correct answer",
            "Submit incorrect answer",
            "Submit empty input",
            "Submit very large number",
            "Submit negative number",
            "Rapid multiple submissions",
            "Refresh page mid-game",
            "Check timer expiration",
            "Check network interruption"
        ]

        # Base test cases
        for i, desc in enumerate(base_tests):
            test_cases.append({
                "id": f"TC_{i+1}",
                "description": desc,
                "steps": ["Open game URL", desc],
                "expected_result": "Game behaves as expected",
                "priority": "medium"
            })

        # ---- RAG: Add memory-driven tests ----
        past_issues = self.memory.summarize_failures()

        for issue in past_issues:
            test_cases.append({
                "id": f"MEM_{len(test_cases)+1}",
                "description": f"Re-test scenario based on past issue: {issue}",
                "steps": ["Open game URL", issue],
                "expected_result": "Issue should not reoccur",
                "priority": "high"
            })

        return test_cases
