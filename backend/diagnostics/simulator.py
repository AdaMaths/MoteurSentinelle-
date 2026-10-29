"""Simulateur didactique de comportement électromécanique.

Fournit 5 scénarios caractéristiques d'apprentissage :
1. Fonctionnement nominal normal
2. Surcharge mécanique progressive
3. Défaut de ventilation / encrassement
4. Dégradation mécanique de roulement
5. Déséquilibre d'alimentation triphasée

MENTION OBLIGATOIRE SUR TOUS LES RÉSULTATS :
'SIMULÉES — NON ISSUES DE MESURES RÉELLES'
"""

from typing import Dict, Any

class PedagogicalSimulator:
    SCENARIOS = {
        "nominal": {
            "nom": "Fonctionnement Nominal Normal",
            "description": "Moteur asynchrone triphasé 4 pôles (1500 tr/min synchrone, 1450 tr/min nominal), 400V, 5.5 kW, alimenté sous charge nominale équilibrée.",
            "defaults": {"facteur_charge": 1.0, "temp_ambiante": 30.0}
        },
        "surcharge": {
            "nom": "Surcharge Mécanique Progressive",
            "description": "Augmentation anormale du couple résistant imposé par la machine entraînée (ex. bourrage ou frottement dur).",
            "defaults": {"facteur_charge": 1.4, "temp_ambiante": 30.0}
        },
        "ventilation": {
            "nom": "Défaut de Ventilation / Encrassement",
            "description": "Obstruction du capot de ventilation ou encrassement sévère des ailettes de refroidissement.",
            "defaults": {"facteur_charge": 0.8, "etat_ventilation": 0.25}
        },
        "roulement": {
            "nom": "Dégradation Mécanique de Roulement",
            "description": "Usure de la piste de roulement avant consécutive à un défaut de graissage ou désalignement.",
            "defaults": {"usure": 0.8}
        },
        "desequilibre": {
            "nom": "Déséquilibre de Tension d'Alimentation",
            "description": "Dissymétrie de 4% entre les tensions d'alimentation triphasée.",
            "defaults": {"desequilibre_pct": 4.0}
        }
    }

    @classmethod
    def list_scenarios(cls) -> Dict[str, Any]:
        return cls.SCENARIOS

    @classmethod
    def simulate(cls, scenario_id: str, custom_params: Dict[str, Any] = None) -> Dict[str, Any]:
        if scenario_id not in cls.SCENARIOS:
            raise ValueError(f"Scénario inconnu : {scenario_id}")

        params = dict(cls.SCENARIOS[scenario_id]["defaults"])
        if custom_params:
            params.update(custom_params)

        if scenario_id == "nominal":
            i = 11.0
            v = 1450.0
            t = 55.0
            vib = 1.2
            symptomes = ["Fonctionnement silencieux et régulier", "Température stable"]
            exp = "Régime nominal équilibré à pleine charge. Glissement (3.3%) et élévation de température normaux."
        elif scenario_id == "surcharge":
            fc = params.get("facteur_charge", 1.4)
            i = round(11.0 * fc, 1)
            v = 1410.0
            t = round(30.0 + 40.0 * (fc**2), 1)
            vib = 2.8
            symptomes = ["Échauffement anormal de carcasse", "Légère baisse de vitesse", f"Courant ({i} A) supérieur à In (11 A)"]
            exp = f"La surcharge ({int(fc*100)}%) accroît le glissement et fait grimper le courant au-dessus de In. Les pertes Joule augmentent au carré du courant."
        elif scenario_id == "ventilation":
            i = 9.2
            v = 1460.0
            t = 88.5
            vib = 1.4
            symptomes = ["Carcasse très chaude (>85°C) même à charge modérée", "Flux d'air très faible"]
            exp = "L'encrassement thermique bloque la convection forcée : malgré un courant normal, la température s'envole dangereusement."
        elif scenario_id == "roulement":
            i = 11.2
            v = 1445.0
            t = 58.0
            vib = 5.6
            symptomes = ["Bruit de frottement / sifflement au palier avant", "Vibrations anormales (5.6 mm/s RMS)"]
            exp = "L'écaillage des pistes de roulement engendre des chocs périodiques. La vibration dépasse le seuil d'alarme ISO 10816 (4.5 mm/s)."
        elif scenario_id == "desequilibre":
            i = 13.8
            v = 1435.0
            t = 76.0
            vib = 3.6
            symptomes = ["Grognement électromagnétique caractéristique (100 Hz)", "Échauffement asymétrique"]
            exp = "Un déséquilibre de 4% engendre un champ tournant inverse qui freine le rotor et augmente fortement les pertes statoriques."

        return {
            "avertissement_legal": "VALEURS SIMULÉES — NON ISSUES DE MESURES RÉELLES (OUTIL DIDACTIQUE)",
            "scenario": cls.SCENARIOS[scenario_id]["nom"],
            "indicateurs_physiques_simules": {
                "courant_ligne_a": i,
                "vitesse_rotation_trmin": v,
                "temperature_carcasse_c": t,
                "vibration_globale_rms_mms": vib
            },
            "symptomes_observes": symptomes,
            "explication_pedagogique": exp,
            "limites_modele": "Modèle électromécanique d'ordre 1 pédagogique. Ne remplace pas un banc d'essai réel."
        }
