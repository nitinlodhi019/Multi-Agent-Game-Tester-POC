from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents.orchestrator import OrchestratorAgent

app = FastAPI(title="Multi-Agent Game Tester POC")

orchestrator = OrchestratorAgent()

class GameRequest(BaseModel):
    url: str

@app.post("/plan")
async def generate_plan(req: GameRequest):
    plan = orchestrator.generate_plan(req.url)
    return {"status": "ok", "test_cases": plan}

@app.post("/execute")
async def execute_tests(req: GameRequest):
    report = await orchestrator.run_tests(req.url)
    return {"status": "completed", "report": report}

@app.get("/")
def root():
    return {"message": "Multi-Agent Game Tester is running"}
