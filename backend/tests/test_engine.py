import pytest
from diagnostics.engine import DiagnosticEngine

@pytest.fixture
def engine():
    return DiagnosticEngine()

def test_absence_symptomes(engine):
    res = engine.analyze({}, [], {})
    assert res["statut"] == "DONNEES_INSUFFISANTES"
    assert len(res["hypotheses"]) == 0
    assert len(res["avertissements_securite"]) >= 2

def test_symptome_echauffement_et_surcharge(engine):
    res = engine.analyze(
        motor_data={"puissance_kw": 11.0},
        symptoms=["echauffement_anormal", "declenchement_protection"],
        operating_context={"charge_bloquee": True}
    )
    assert res["statut"] == "ANALYSE_COMPLETE"
    assert len(res["hypotheses"]) >= 1
    causes = [h["cause"] for h in res["hypotheses"]]
    assert any("surcharge" in c.lower() for c in causes)

def test_symptome_roulement(engine):
    res = engine.analyze(
        motor_data={},
        symptoms=["bruit_anormal", "vibration_excessive"],
        operating_context={"manque_graissage": True}
    )
    causes = [h["cause"] for h in res["hypotheses"]]
    assert any("roulement" in c.lower() for c in causes)
    hyp_roulement = next(h for h in res["hypotheses"] if "roulement" in h["cause"].lower())
    assert hyp_roulement["indice_pertinence"] > 50

def test_contradiction_detectee(engine):
    res = engine.analyze(
        motor_data={},
        symptoms=["baisse_vitesse"],
        operating_context={"charge_moteur": "a_vide"}
    )
    assert len(res["contradictions"]) >= 1
