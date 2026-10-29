"""Module de sécurité industrielle et consignation électrique pour MoteurSentinelle.

Règles fondamentales :
- Jamais d'intervention sous tension préconisée à un non-professionnel.
- Respect strict des 5 étapes de la consignation électrique (NF C 18-510 / standard international).
- Interdiction absolue de shunter ou neutraliser un organe de protection.
"""

from typing import List, Dict, Any

class SafetyEngine:
    CONSIGNATION_STEPS = [
        {"etape": 1, "titre": "Séparation", "description": "Ouvrir et séparer visiblement l'appareil de sectionnement principal (sectionneur ou disjoncteur)."},
        {"etape": 2, "titre": "Condamnation", "description": "Verrouiller le sectionneur en position ouverte par un cadenas de consignation et apposer une pancarte d'interdiction de manœuvrer."},
        {"etape": 3, "titre": "Identification", "description": "Vérifier que l'installation consignée correspond exactement au moteur concerné (repérage de ligne)."},
        {"etape": 4, "titre": "Vérification d'Absence de Tension (VAT)", "description": "Effectuer la VAT sur les 3 phases et la terre avec un appareil vérificateur normalisé (VAT), testé avant et après mesure."},
        {"etape": 5, "titre": "Mise à la terre et en court-circuit (MALT/CC)", "description": "Raccorder la mise à la terre et en court-circuit immédiate si requis par le niveau de tension ou la proximité de conducteurs voisins."}
    ]

    @staticmethod
    def get_mandatory_warnings(symptoms: List[str], context: Dict[str, Any]) -> List[Dict[str, str]]:
        warnings = [
            {
                "niveau": "CRITIQUE",
                "titre": "Règle de consignation obligatoire",
                "message": "Toute intervention mécanique ou ouverture de boîte à bornes exige la consignation électrique complète préalable et la Vérification d'Absence de Tension (VAT)."
            },
            {
                "niveau": "INTERDICTION",
                "titre": "Non-neutralisation des protections",
                "message": "Il est formellement interdit de réarmer aveuglément ou de shunter un relais thermique ou un disjoncteur magnétothermique qui a déclenché."
            }
        ]

        if "odeur_brule" in symptoms:
            warnings.append({
                "niveau": "DANGER_IMMEDIAT",
                "titre": "Risque d'incendie et court-circuit franc",
                "message": "Couper immédiatement l'alimentation générale en amont. Ne pas approcher le moteur sans équipement de protection individuel (EPI) adapté."
            })

        if "vibration_excessive" in symptoms:
            warnings.append({
                "niveau": "AVERTISSEMENT",
                "titre": "Risque de rupture mécanique",
                "message": "Ne pas stationner dans le plan de rotation de l'accouplement. Arrêter l'équipement pour éviter l'endommagement irréversible des paliers et de l'arbre."
            })

        if "echauffement_anormal" in symptoms:
            warnings.append({
                "niveau": "ATTENTION",
                "titre": "Risque de brûlure thermique",
                "message": "La carcasse peut dépasser 90°C. Ne jamais toucher la carcasse à main nue. Utiliser un thermomètre infrarouge ou pyromètre étalonné."
            })

        return warnings
