"""Persistance SQLite locale avec schéma relationnel durable."""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class DataStorage:
    def __init__(self, db_path: str = "moteursentinelle.db"):
        self.db_path = db_path
        self._init_sqlite()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_sqlite(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS motors (
                    id TEXT PRIMARY KEY,
                    designation TEXT NOT NULL,
                    type_moteur TEXT,
                    puissance_kw REAL,
                    tension_nominale_v TEXT,
                    courant_nominal_a REAL,
                    vitesse_nominale_trmin REAL,
                    equipement_entraine TEXT,
                    date_enregistrement TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS diagnostics (
                    id TEXT PRIMARY KEY,
                    moteur_id TEXT,
                    date_diagnostic TEXT,
                    symptomes TEXT,
                    hypotheses TEXT,
                    technicien TEXT,
                    statut TEXT
                )
            """)
            conn.commit()

            cursor.execute("SELECT COUNT(*) FROM motors")
            if cursor.fetchone()[0] == 0:
                demo_motor = (
                    "MOT-SN-001",
                    "Moteur Broyeur Principal - Usine Rufisque",
                    "Asynchrone triphasé à cage",
                    11.0,
                    "400V Triphasé",
                    21.5,
                    1465.0,
                    "Broyeur à marteaux",
                    datetime.now().isoformat()
                )
                cursor.execute("""
                    INSERT INTO motors VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, demo_motor)
                conn.commit()

    def list_motors(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM motors ORDER BY date_enregistrement DESC")
            return [dict(r) for r in cursor.fetchall()]

    def save_diagnostic(self, diag_id: str, moteur_id: Optional[str], symptomes: List[str], hypotheses: List[Dict[str, Any]], technicien: str = "Technicien") -> Dict[str, Any]:
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO diagnostics VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                diag_id,
                moteur_id,
                now,
                json.dumps(symptomes, ensure_ascii=False),
                json.dumps(hypotheses, ensure_ascii=False),
                technicien,
                "Enregistré"
            ))
            conn.commit()
            return {"id": diag_id, "date_diagnostic": now, "statut": "Enregistré"}

    def list_diagnostics(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM diagnostics ORDER BY date_diagnostic DESC")
            rows = cursor.fetchall()
            output = []
            for r in rows:
                item = dict(r)
                item["symptomes"] = json.loads(item["symptomes"]) if item["symptomes"] else []
                item["hypotheses"] = json.loads(item["hypotheses"]) if item["hypotheses"] else []
                output.append(item)
            return output
