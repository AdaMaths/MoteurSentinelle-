/**
 * Client API pour MoteurSentinelle.
 */
const isLocalDevelopment = ["localhost", "127.0.0.1"].includes(window.location.hostname);
const API_BASE_URL = isLocalDevelopment ? "http://localhost:8000/api" : "/api";

const MotorAPI = {
    async checkHealth() {
        try {
            const res = await fetch(`${API_BASE_URL}/health`, { signal: AbortSignal.timeout(2000) });
            return await res.json();
        } catch (e) {
            return null;
        }
    },

    async getStats() {
        try {
            const res = await fetch(`${API_BASE_URL}/dashboard/stats`);
            return await res.json();
        } catch (e) {
            return { nb_moteurs: 1, nb_diagnostics: 0, derniers_diagnostics: [] };
        }
    },

    async analyzeDiagnostic(payload) {
        try {
            const res = await fetch(`${API_BASE_URL}/diagnostics/analyze`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            return await res.json();
        } catch (e) {
            return null;
        }
    },

    async saveDiagnostic(payload) {
        try {
            const res = await fetch(`${API_BASE_URL}/diagnostics`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            return await res.json();
        } catch (e) {
            return null;
        }
    },

    async getDiagnostics() {
        try {
            const res = await fetch(`${API_BASE_URL}/diagnostics`);
            return await res.json();
        } catch (e) {
            return [];
        }
    },

    async getMotors() {
        try {
            const res = await fetch(`${API_BASE_URL}/motors`);
            return await res.json();
        } catch (e) {
            return [{ id: "MOT-SN-001", designation: "Moteur Broyeur Rufisque", puissance_kw: 11.0, courant_nominal_a: 21.5, vitesse_nominale_trmin: 1465 }];
        }
    },

    async runSimulation(scenarioId) {
        try {
            const res = await fetch(`${API_BASE_URL}/simulation/run?scenario_id=${scenarioId}`, { method: "POST" });
            return await res.json();
        } catch (e) {
            return null;
        }
    }
};
