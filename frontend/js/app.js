/**
 * Contrôleur d'interface utilisateur MoteurSentinelle.
 */
document.addEventListener("DOMContentLoaded", async () => {
    // 1. Navigation par onglets
    const navButtons = document.querySelectorAll(".nav-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            navButtons.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));
            btn.classList.add("active");
            const target = btn.getAttribute("data-tab");
            const targetPane = document.getElementById(target);
            if (targetPane) targetPane.classList.add("active");

            if (target === "tab-history") loadDiagnosticsHistory();
            if (target === "tab-motors") loadMotors();
        });
    });

    // 2. Vérification connectivité API
    const health = await MotorAPI.checkHealth();
    const statusText = document.getElementById("status-text");
    if (health) {
        statusText.textContent = "Connecté à l'API Python";
    } else {
        statusText.textContent = "API non démarrée (Lancez app.py)";
        statusText.style.color = "#ef4444";
    }

    loadDashboardStats();

    // 3. Diagnostic Guidé
    document.getElementById("btn-run-diag").addEventListener("click", async () => {
        const motorId = document.getElementById("diag-motor-select").value;
        const techName = document.getElementById("diag-tech-name").value;
        const selectedSymptoms = Array.from(document.querySelectorAll("input[name='symptom']:checked")).map(cb => cb.value);

        const context = {
            capot_obstrue: document.getElementById("ctx-capot-obstrue").checked,
            charge_bloquee: document.getElementById("ctx-charge-bloquee").checked,
            reseau_instable: document.getElementById("ctx-reseau-instable").checked,
            manque_graissage: document.getElementById("ctx-manque-graissage").checked
        };

        const payload = {
            moteur_id: motorId,
            nom_technicien: techName,
            symptomes: selectedSymptoms,
            contexte_fonctionnement: context
        };

        const res = await MotorAPI.saveDiagnostic(payload);
        const container = document.getElementById("diagnostic-results-container");
        container.classList.remove("hidden");

        if (!res || !res.resultat) {
            container.innerHTML = `<p style="color:#ef4444;">Impossible de joindre l'API. Assurez-vous que <code>python backend/app.py</code> est lancé.</p>`;
            return;
        }

        const data = res.resultat;
        let html = `<h3>Résultats de l'analyse déterministe (ID : ${res.diagnostic.id})</h3>`;

        // Sécurité
        if (data.avertissements_securite && data.avertissements_securite.length) {
            html += `<div class="safety-alert-box"><h4>⚠️ Consignes de sécurité obligatoires</h4><ul class="clean-list">`;
            data.avertissements_securite.forEach(w => {
                html += `<li><strong>${w.titre} :</strong> ${w.message}</li>`;
            });
            html += `</ul></div>`;
        }

        // Hypothèses
        if (data.hypotheses && data.hypotheses.length) {
            data.hypotheses.forEach(hyp => {
                html += `
                    <div class="hypothesis-card">
                        <div class="hyp-header">
                            <span class="hyp-title">🔍 ${hyp.cause}</span>
                            <span class="hyp-score">Pertinence : ${hyp.indice_pertinence} / 100</span>
                        </div>
                        <p style="font-size:0.88rem; margin-bottom:6px;">${hyp.description}</p>
                        <p style="font-size:0.8rem; color:#94a3b8;"><strong>Indices :</strong> ${hyp.indices_favorables.join(", ")}</p>
                        <div style="font-size:0.82rem; margin-top:6px; color:#38bdf8;">
                            <strong>Contrôles recommandés :</strong>
                            <ul class="clean-list">
                                ${hyp.controles_recommandes.map(c => `<li>${c}</li>`).join("")}
                            </ul>
                        </div>
                    </div>
                `;
            });
        } else {
            html += `<p>Aucune anomalie franche détectée. Données insuffisantes pour statuer.</p>`;
        }

        container.innerHTML = html;
        loadDashboardStats();
    });

    // 4. Simulateur Pédagogique
    document.getElementById("btn-simulate").addEventListener("click", async () => {
        const scenario = document.getElementById("sim-scenario-select").value;
        const res = await MotorAPI.runSimulation(scenario);
        if (!res) return;

        const phys = res.indicateurs_physiques_simules;
        document.getElementById("sim-val-current").textContent = `${phys.courant_ligne_a} A`;
        document.getElementById("sim-val-speed").textContent = `${phys.vitesse_rotation_trmin} tr/min`;
        document.getElementById("sim-val-temp").textContent = `${phys.temperature_carcasse_c} °C`;
        document.getElementById("sim-val-vib").textContent = `${phys.vibration_globale_rms_mms} mm/s`;

        document.getElementById("sim-explanation-text").textContent = res.explication_pedagogique;
    });

    // Fonctions de chargement
    async function loadDashboardStats() {
        const stats = await MotorAPI.getStats();
        document.getElementById("kpi-motors").textContent = stats.nb_moteurs || 1;
        document.getElementById("kpi-diags").textContent = stats.nb_diagnostics || 0;
    }

    async function loadMotors() {
        const motors = await MotorAPI.getMotors();
        const container = document.getElementById("motors-list-container");
        let html = `<table><thead><tr><th>ID</th><th>Désignation</th><th>Puissance</th><th>In (A)</th><th>Vitesse</th></tr></thead><tbody>`;
        motors.forEach(m => {
            html += `<tr><td><strong>${m.id}</strong></td><td>${m.designation}</td><td>${m.puissance_kw} kW</td><td>${m.courant_nominal_a} A</td><td>${m.vitesse_nominale_trmin} tr/min</td></tr>`;
        });
        html += `</tbody></table>`;
        container.innerHTML = html;
    }

    async function loadDiagnosticsHistory() {
        const diags = await MotorAPI.getDiagnostics();
        const container = document.getElementById("history-table-container");
        if (!diags || !diags.length) {
            container.innerHTML = "<p>Aucun diagnostic dans la base de données.</p>";
            return;
        }
        let html = `<table><thead><tr><th>ID</th><th>Date</th><th>Moteur</th><th>Symptômes</th><th>Hypothèse principale</th></tr></thead><tbody>`;
        diags.forEach(d => {
            const hyp = d.hypotheses && d.hypotheses[0] ? d.hypotheses[0].cause : "--";
            html += `<tr><td>${d.id}</td><td>${(d.date_diagnostic || "").slice(0, 10)}</td><td>${d.moteur_id}</td><td>${(d.symptomes || []).join(", ")}</td><td>${hyp}</td></tr>`;
        });
        html += `</tbody></table>`;
        container.innerHTML = html;
    }
});
