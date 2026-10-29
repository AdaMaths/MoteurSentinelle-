"""Application FastAPI principale pour MoteurSentinelle."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os

from api.models import DiagnosticRequest, MotorCreate
from diagnostics.engine import DiagnosticEngine
from diagnostics.simulator import PedagogicalSimulator
from services.storage import DataStorage

app = FastAPI(
    title="MoteurSentinelle API",
    description="API de diagnostic électromécanique explicable et de fiabilité",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = DiagnosticEngine()
storage = DataStorage(db_path=os.getenv("DATABASE_PATH", "moteursentinelle.db"))

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "MoteurSentinelle API",
        "version": "1.0.0",
        "persistence": "SQLite Local Active"
    }

@app.get("/api/dashboard/stats")
def stats():
    motors = storage.list_motors()
    diags = storage.list_diagnostics()
    return {
        "nb_moteurs": len(motors),
        "nb_diagnostics": len(diags),
        "derniers_diagnostics": diags[:5]
    }

@app.post("/api/diagnostics/analyze")
def analyze(req: DiagnosticRequest):
    return engine.analyze({"id": req.moteur_id}, req.symptomes, req.contexte_fonctionnement)

@app.post("/api/diagnostics")
def save_diagnostic(req: DiagnosticRequest):
    result = engine.analyze({"id": req.moteur_id}, req.symptomes, req.contexte_fonctionnement)
    diag_id = f"DIAG-{uuid.uuid4().hex[:6].upper()}"
    saved = storage.save_diagnostic(
        diag_id=diag_id,
        moteur_id=req.moteur_id,
        symptomes=req.symptomes,
        hypotheses=result["hypotheses"],
        technicien=req.nom_technicien or "Technicien"
    )
    return {"diagnostic": saved, "resultat": result}

@app.get("/api/diagnostics")
def get_diagnostics():
    return storage.list_diagnostics()

@app.get("/api/motors")
def get_motors():
    return storage.list_motors()

@app.get("/api/simulation/scenarios")
def get_scenarios():
    return PedagogicalSimulator.list_scenarios()

@app.post("/api/simulation/run")
def run_simulation(scenario_id: str, custom_params: dict = None):
    try:
        return PedagogicalSimulator.simulate(scenario_id, custom_params)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
