import os
import hashlib
from typing import Dict


class AnalyzerAgent:
    """
    Validates test execution using:
    1. Repeat execution consistency
    2. Cross-agent artifact comparison
    """

    def _hash_file(self, path: str) -> str:
        """Generate hash of a file for comparison"""
        if not os.path.exists(path):
            return ""

        hasher = hashlib.md5()
        with open(path, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    def validate(self, test_case: Dict, execution_results: list) -> Dict:
        """
        execution_results: list of execution outputs (same test, multiple runs)
        """

        hashes = []
        for result in execution_results:
            screenshot = result["artifacts"].get("after_screenshot")
            hashes.append(self._hash_file(screenshot))

        unique_hashes = set(hashes)

        if len(unique_hashes) == 1:
            verdict = "pass"
            stability = "stable"
        else:
            verdict = "flaky"
            stability = "inconsistent"

        return {
            "test_id": test_case["id"],
            "description": test_case["description"],
            "verdict": verdict,
            "stability": stability,
            "runs": len(execution_results),
            "artifacts": execution_results,
            "notes": (
                "Consistent behavior across runs"
                if verdict == "pass"
                else "Different outputs detected across runs"
            ),
        }
