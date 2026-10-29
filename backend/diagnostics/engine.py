"""Moteur de diagnostic déterministe et explicable pour MoteurSentinelle.

Principes fondamentaux :
- AUCUNE probabilité statistique inventée ou fausse certitude.
- Score heuristique d'adéquation des règles clairement expliqué comme un rang de pertinence.
- Détection des données contradictoires ou insuffisantes.
- Traçabilité complète du raisonnement pour l'apprentissage technique.
"""

from typing import List, Dict, Any
from .rules import RULES_DATABASE
from .safety import SafetyEngine

class DiagnosticEngine:
    def __init__(self):
        self.rules = RULES_DATABASE

    def analyze(self, motor_data: Dict[str, Any], symptoms: List[str], operating_context: Dict[str, Any]) -> Dict[str, Any]:
        if not symptoms:
            return {
                "statut": "DONNEES_INSUFFISANTES",
                "message": "Aucun symptôme n'a été sélectionné. Le diagnostic ne peut pas être établi.",
                "hypotheses": [],
                "donnees_manquantes": ["Sélection d'au moins un symptôme observé"],
                "avertissements_securite": SafetyEngine.get_mandatory_warnings([], operating_context),
                "controles_prioritaires": ["Réaliser une observation attentive des conditions de fonctionnement."]
            }

        contradictions = []
        if "baisse_vitesse" in symptoms and operating_context.get("charge_moteur") == "a_vide":
            contradictions.append("Une baisse de vitesse importante à vide sans bruit mécanique anormal est atypique pour un moteur sain.")

        hypotheses = []
        missing_data_global = set()

        for rule in self.rules:
            indices_favorables = []
            score_pertinence = 0

            # 1. Correspondance avec les symptômes
            matched_symptoms = [s for s in rule["symptomes_declencheurs"] if s in symptoms]
            if matched_symptoms:
                score_pertinence += rule["poids_base"] * len(matched_symptoms)
                indices_favorables.append(f"Symptôme(s) concordant(s) : {', '.join(matched_symptoms)}")

            # 2. Facteurs contextuels aggravants
            matched_context = [ctx for ctx in rule["facteurs_aggravants"] if operating_context.get(ctx)]
            if matched_context:
                score_pertinence += 25 * len(matched_context)
                indices_favorables.append(f"Facteur(s) contextuel(s) aggravant(s) : {', '.join(matched_context)}")

            if indices_favorables:
                missing_for_rule = ["Mesure de courant de ligne (In)", "Contrôle visuel direct"]
                for m in missing_for_rule:
                    missing_data_global.add(m)

                hypotheses.append({
                    "id_regle": rule["id"],
                    "cause": rule["cause"],
                    "description": rule["description"],
                    "indice_pertinence": min(score_pertinence, 100),
                    "nature_indice": "Score heuristique d'adéquation logique (NON probabiliste)",
                    "indices_favorables": indices_favorables,
                    "donnees_manquantes": missing_for_rule,
                    "controles_recommandes": rule["controles_recommandes"],
                    "limites_diagnostic": rule["limites"]
                })

        hypotheses.sort(key=lambda h: h["indice_pertinence"], reverse=True)

        return {
            "statut": "ANALYSE_COMPLETE",
            "message": f"{len(hypotheses)} hypothèse(s) formulée(s) par le moteur de règles déterministe.",
            "hypotheses": hypotheses,
            "contradictions": contradictions,
            "donnees_manquantes": sorted(list(missing_data_global)),
            "avertissements_securite": SafetyEngine.get_mandatory_warnings(symptoms, operating_context),
            "controles_prioritaires": hypotheses[0]["controles_recommandes"] if hypotheses else []
        }
