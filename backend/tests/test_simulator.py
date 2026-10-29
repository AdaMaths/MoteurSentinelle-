import pytest
from diagnostics.simulator import PedagogicalSimulator

def test_list_scenarios():
    sc = PedagogicalSimulator.list_scenarios()
    assert len(sc) == 5
    assert "nominal" in sc
    assert "surcharge" in sc
    assert "ventilation" in sc
    assert "roulement" in sc
    assert "desequilibre" in sc

def test_scenario_nominal():
    res = PedagogicalSimulator.simulate("nominal")
    assert "SIMULÉES" in res["avertissement_legal"]
    assert res["indicateurs_physiques_simules"]["courant_ligne_a"] == 11.0
    assert res["indicateurs_physiques_simules"]["vitesse_rotation_trmin"] == 1450.0

def test_scenario_surcharge():
    res = PedagogicalSimulator.simulate("surcharge")
    assert res["indicateurs_physiques_simules"]["courant_ligne_a"] > 11.0
    assert res["indicateurs_physiques_simules"]["temperature_carcasse_c"] > 70.0

def test_scenario_invalide():
    with pytest.raises(ValueError):
        PedagogicalSimulator.simulate("inconnu")
