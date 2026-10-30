"""Persistance Firestore via le SDK Firebase Admin."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import firebase_admin
from firebase_admin import credentials, firestore

FIRESTORE_REQUEST_TIMEOUT_SECONDS = 10


class FirestoreStorage:
    def __init__(self, project_id: Optional[str] = None):
        project_id = project_id or os.getenv("FIREBASE_PROJECT_ID")
        if not project_id:
            raise ValueError("FIREBASE_PROJECT_ID is required when DATABASE_TYPE=firestore")

        try:
            app = firebase_admin.get_app()
        except ValueError:
            service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
            credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if service_account_json:
                certificate = credentials.Certificate(json.loads(service_account_json))
            elif credential_path:
                path = Path(credential_path)
                if not path.is_absolute():
                    path = Path(__file__).resolve().parents[2] / path
                if not path.is_file():
                    raise FileNotFoundError(
                        f"Firebase service account file not found: {path}"
                    )
                certificate = credentials.Certificate(str(path))
            else:
                certificate = None
            app = firebase_admin.initialize_app(
                credential=certificate,
                options={"projectId": project_id},
            )

        self.db = firestore.client(app=app)
        self.motors = self.db.collection("motors")
        self.diagnostics = self.db.collection("diagnostics")
        self._demo_motor_seeded = False

    def _seed_demo_motor(self) -> None:
        demo_motor = {
            "id": "MOT-SN-001",
            "designation": "Moteur Broyeur Principal - Usine Rufisque",
            "type_moteur": "Asynchrone triphasé à cage",
            "puissance_kw": 11.0,
            "tension_nominale_v": "400V Triphasé",
            "courant_nominal_a": 21.5,
            "vitesse_nominale_trmin": 1465.0,
            "equipement_entraine": "Broyeur à marteaux",
            "date_enregistrement": datetime.now().isoformat(),
        }
        motor_ref = self.motors.document(demo_motor["id"])
        if not motor_ref.get(timeout=FIRESTORE_REQUEST_TIMEOUT_SECONDS).exists:
            motor_ref.set(demo_motor, timeout=FIRESTORE_REQUEST_TIMEOUT_SECONDS)

    def list_motors(self) -> List[Dict[str, Any]]:
        if not self._demo_motor_seeded:
            self._seed_demo_motor()
            self._demo_motor_seeded = True
        motors = [
            snapshot.to_dict()
            for snapshot in self.motors.stream(timeout=FIRESTORE_REQUEST_TIMEOUT_SECONDS)
        ]
        return sorted(
            motors,
            key=lambda motor: motor.get("date_enregistrement", ""),
            reverse=True,
        )

    def save_diagnostic(
        self,
        diag_id: str,
        moteur_id: Optional[str],
        symptomes: List[str],
        hypotheses: List[Dict[str, Any]],
        technicien: str = "Technicien",
    ) -> Dict[str, Any]:
        now = datetime.now().isoformat()
        diagnostic = {
            "id": diag_id,
            "moteur_id": moteur_id,
            "date_diagnostic": now,
            "symptomes": symptomes,
            "hypotheses": hypotheses,
            "technicien": technicien,
            "statut": "Enregistré",
        }
        self.diagnostics.document(diag_id).create(
            diagnostic, timeout=FIRESTORE_REQUEST_TIMEOUT_SECONDS
        )
        return {"id": diag_id, "date_diagnostic": now, "statut": "Enregistré"}

    def list_diagnostics(self) -> List[Dict[str, Any]]:
        diagnostics = [
            snapshot.to_dict()
            for snapshot in self.diagnostics.stream(
                timeout=FIRESTORE_REQUEST_TIMEOUT_SECONDS
            )
        ]
        return sorted(
            diagnostics,
            key=lambda diagnostic: diagnostic.get("date_diagnostic", ""),
            reverse=True,
        )
