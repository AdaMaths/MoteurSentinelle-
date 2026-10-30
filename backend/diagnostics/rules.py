"""Définition des règles électromécaniques déterministes.
Chaque règle explicite ses conditions d'activation, ses indices favorables,
les données manquantes et les contrôles recommandés.
"""

RULES_DATABASE = [
    {
        "id": "RULE_SURCHARGE_MECANIQUE",
        "cause": "Surcharge mécanique anormale",
        "description": "Le moteur est soumis à un couple résistant supérieur à son couple nominal, entraînant une surintensité et un échauffement global.",
        "symptomes_declencheurs": ["echauffement_anormal", "declenchement_protection", "baisse_vitesse"],
        "facteurs_aggravants": ["charge_bloquee", "courant_eleve"],
        "controles_recommandes": [
            "Contrôle à vide : désaccoupler le moteur de la machine entraînée et vérifier la libre rotation manuelle de l'arbre (hors tension).",
            "Mesure du courant de ligne sur les 3 phases avec une pince multimètre étalonnée et comparaison au courant nominal (In) de la plaque.",
            "Vérification de l'organe entraîné (grippage de pompe, bourrage de convoyeur, roulements machine usés)."
        ],
        "limites": "Ne peut pas être confirmé avec certitude sans mesure effective du courant absorbé sous charge.",
        "poids_base": 30
    },
    {
        "id": "RULE_DEFAUT_VENTILATION",
        "cause": "Ventilation ou refroidissement insuffisant",
        "description": "L'évacuation calorifique est entravée, provoquant une montée thermique excessive même à charge normale ou réduite.",
        "symptomes_declencheurs": ["echauffement_anormal"],
        "facteurs_aggravants": ["capot_obstrue", "environnement_poussiereux"],
        "controles_recommandes": [
            "Inspection visuelle du capot de ventilateur et nettoyage des grilles d'aspiration d'air.",
            "Vérification de la propreté des ailettes de refroidissement de la carcasse (dépôt de poussière ou graisse).",
            "Contrôle de la fixation mécanique et du sens de rotation de l'hélice de ventilation arrière."
        ],
        "limites": "Un échauffement localisé sur un palier indique plutôt un roulement qu'un défaut de ventilation globale.",
        "poids_base": 25
    },
    {
        "id": "RULE_DEFAUT_ROULEMENT",
        "cause": "Anomalie mécanique de roulement ou d'alignement",
        "description": "Détérioration de la piste, des billes/rouleaux, défaut de lubrification ou défaut d'alignement d'accouplement.",
        "symptomes_declencheurs": ["bruit_anormal", "vibration_excessive", "grognement"],
        "facteurs_aggravants": ["manque_graissage", "choc_mecanique"],
        "controles_recommandes": [
            "Écoute au stéthoscope mécanique ou tournevis d'écoute sur les flasques avant et arrière.",
            "Contrôle du jeu radial et axial au comparateur sur l'arbre moteur.",
            "Mesure de vibration globale (vitesse efficace RMS en mm/s selon norme ISO 10816-3).",
            "Vérification de l'alignement laser ou au comparateur de l'accouplement moteur/charge."
        ],
        "limites": "La distinction entre défaut de bague intérieure, extérieure ou désalignement nécessite une analyse spectrale FFT.",
        "poids_base": 30
    },
    {
        "id": "RULE_DESEQUILIBRE_ALIMENTATION",
        "cause": "Déséquilibre des tensions ou perte d'une phase",
        "description": "Une dissymétrie des tensions d'alimentation crée un champ tournant inverse destructeur, induisant de fortes vibrations et un échauffement sévère du stator.",
        "symptomes_declencheurs": ["grognement", "declenchement_protection", "demarrage_difficile", "echauffement_anormal"],
        "facteurs_aggravants": ["reseau_instable"],
        "controles_recommandes": [
            "Mesure des 3 tensions simples et composées aux bornes du moteur en fonctionnement (V12, V23, V31).",
            "Calcul du taux de déséquilibre : si supérieur à 1-2 %, l'échauffement augmente de façon exponentielle.",
            "Vérification de la chute de tension aux pôles du contacteur de ligne et état des fusibles amont."
        ],
        "limites": "Nécessite impérativement des mesures électriques sous tension par une personne habilitée avec EPI.",
        "poids_base": 35
    },
    {
        "id": "RULE_DEFAUT_ISOLEMENT_BOBINAGE",
        "cause": "Défaut d'isolement ou court-circuit entre spires",
        "description": "Dégradation du vernis isolant des enroulements suite à une surcharge thermique, surtension ou humidité.",
        "symptomes_declencheurs": ["declenchement_protection", "odeur_brule"],
        "facteurs_aggravants": ["humidite_elevee", "moteur_ancien"],
        "controles_recommandes": [
            "Mesure de la résistance d'isolement au mégohmmètre (500V ou 1000V DC) entre chaque phase et la carcasse (consignation obligatoire).",
            "Mesure des résistances d'enroulements au milliohmmètre entre U1-U2, V1-V2, W1-W2 pour vérifier la symétrie ohmique.",
            "Inspection visuelle du bobinage après démontage (traces de brûlure, noircissement du vernis)."
        ],
        "limites": "Un court-circuit entre quelques spires d'une même phase ne se détecte pas toujours au mégohmmètre standard.",
        "poids_base": 40
    }
]
