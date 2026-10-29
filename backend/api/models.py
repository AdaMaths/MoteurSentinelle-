from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class MotorCreate(BaseModel):
    identifiant_interne: str = Field(..., example="MOT-ATELIER-01")
    designation: str = Field(..., example="Moteur Pompe d'Exhaure Nord")
    type_moteur: str = Field(default="Asynchrone triphasé à cage")
    marque: Optional[str] = Field(default=None, example="Leroy-Somer")
    modele: Optional[str] = Field(default=None, example="LSES 132 SM")
    puissance_kw: Optional[float] = Field(default=None, ge=0.1, le=1000.0)
    tension_nominale_v: Optional[str] = Field(default="400V Triphasé")
    courant_nominal_a: Optional[float] = Field(default=None, ge=0.1)
    frequence_hz: Optional[float] = Field(default=50.0)
    vitesse_nominale_trmin: Optional[float] = Field(default=1450.0)
    equipement_entraine: Optional[str] = Field(default=None, example="Pompe centrifuge")
    observations: Optional[str] = None

class DiagnosticRequest(BaseModel):
    moteur_id: Optional[str] = "MOT-SN-001"
    symptomes: List[str] = Field(default_factory=list)
    contexte_fonctionnement: Dict[str, Any] = Field(default_factory=dict)
    nom_technicien: Optional[str] = "Technicien Atelier"

class InterventionCreate(BaseModel):
    reference: str = Field(..., example="INT-2026-001")
    moteur_id: str
    symptome_initial: str
    constats: str
    actions_realisees: str
    pieces_remplacees: Optional[str] = None
    resultat: str = Field(..., example="Résolu - Remise en service validée")
    recommandations_suivi: Optional[str] = None
    statut: str = Field(default="Terminée")
