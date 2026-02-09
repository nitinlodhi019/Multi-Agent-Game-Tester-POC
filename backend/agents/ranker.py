from typing import List, Dict

class RankerAgent:
    """
    Ranks test cases based on simple heuristic scoring
    """

    def rank(self, test_cases: List[Dict]) -> List[Dict]:
        for tc in test_cases:
            score = 0

            # Simple scoring rules (POC-friendly)
            if "incorrect" in tc["description"].lower():
                score += 3
            if "empty" in tc["description"].lower():
                score += 2
            if "large" in tc["description"].lower():
                score += 2
            if "timer" in tc["description"].lower():
                score += 2
            if "network" in tc["description"].lower():
                score += 3

            tc["score"] = score

        # Sort descending by score
        ranked = sorted(test_cases, key=lambda x: x["score"], reverse=True)
        return ranked
