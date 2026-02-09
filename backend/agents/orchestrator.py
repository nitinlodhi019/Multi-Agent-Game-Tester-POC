import json
import os
from datetime import datetime

from backend.rag.memory_store import MemoryStore
from backend.agents.planner import PlannerAgent
from backend.agents.ranker import RankerAgent
from backend.agents.executor import ExecutorAgent
from backend.agents.analyzer import AnalyzerAgent


class OrchestratorAgent:

    def __init__(self):
        self.planner = PlannerAgent()
        self.ranker = RankerAgent()
        self.executor = ExecutorAgent()
        self.analyzer = AnalyzerAgent()
        self.memory = MemoryStore()

    def generate_plan(self, url: str):
        test_cases = self.planner.generate_test_cases(url)
        ranked = self.ranker.rank(test_cases)
        return ranked

    async def run_tests(self, url: str):
        test_cases = self.generate_plan(url)
        top_tests = test_cases[:10]

        results = []

        for tc in top_tests:
            run1 = await self.executor.execute_test(url, tc)
            run2 = await self.executor.execute_test(url, tc)

            analysis = self.analyzer.validate(tc, [run1, run2])
            results.append(analysis)

        final_report = {
            "url": url,
            "executed_at": datetime.utcnow().isoformat(),
            "total_tests": len(top_tests),
            "results": results
        }

        # ---- SAVE REPORT TO FILE ----
        os.makedirs("backend/reports", exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        report_path = f"backend/reports/report_{timestamp}.json"

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(final_report, f, indent=2)

        # Attach path for API response
        final_report["report_path"] = report_path

        # ---- SAVE RESULTS TO RAG MEMORY ----
        memory_entries = []

        for r in results:
            memory_entries.append({
                "test_id": r["test_id"],
                "description": r["description"],
                "verdict": r["verdict"],
                "stability": r["stability"],
                "notes": r["notes"]
            })

        self.memory.write(memory_entries)

        return final_report


