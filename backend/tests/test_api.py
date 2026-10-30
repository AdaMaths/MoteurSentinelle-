import os

os.environ["DATABASE_TYPE"] = "sqlite"

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_diag_analyze():
    res = client.post("/api/diagnostics/analyze", json={
        "symptomes": ["echauffement_anormal"],
        "contexte_fonctionnement": {"capot_obstrue": True}
    })
    assert res.status_code == 200
    data = res.json()
    assert data["statut"] == "ANALYSE_COMPLETE"
    assert len(data["hypotheses"]) >= 1

def test_diag_save_and_list():
    res = client.post("/api/diagnostics", json={
        "moteur_id": "MOT-SN-001",
        "symptomes": ["vibration_excessive"],
        "contexte_fonctionnement": {"manque_graissage": True}
    })
    assert res.status_code == 200
    diag_id = res.json()["diagnostic"]["id"]

    res_list = client.get("/api/diagnostics")
    assert res_list.status_code == 200
    diags = res_list.json()
    assert any(d["id"] == diag_id for d in diags)
