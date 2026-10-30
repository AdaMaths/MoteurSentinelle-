/* =========================================
   MOTEURSENTINELLE — ANIMATIONS & MICRO-UX
   ========================================= */

document.addEventListener("DOMContentLoaded", () => {

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    /* Effet de lumière suivant le curseur — Bibliothèque */
    document.querySelectorAll(".knowledge-card").forEach((card) => {
        card.addEventListener("mousemove", (event) => {
            if (reduceMotion) return;

            const rect = card.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            card.style.setProperty("--x", `${x}px`);
            card.style.setProperty("--y", `${y}px`);
        });
    });

    /* Réinitialise l’animation lors du changement d’onglet */
    const navButtons = document.querySelectorAll(".nav-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    navButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.dataset.tab;
            const targetPane = document.getElementById(targetId);

            if (!targetPane) return;

            tabPanes.forEach((pane) => {
                pane.classList.remove("active");
            });

            /* Force le redémarrage de l’animation d’entrée */
            targetPane.classList.remove("active");
            void targetPane.offsetWidth;
            targetPane.classList.add("active");
        });
    });

    /* Animation d’apparition des résultats de diagnostic */
    const resultsContainer = document.getElementById(
        "diagnostic-results-container"
    );

    if (resultsContainer) {
        const observer = new MutationObserver(() => {
            if (!resultsContainer.classList.contains("hidden")) {
                resultsContainer.style.animation = "none";
                void resultsContainer.offsetWidth;
                resultsContainer.style.animation = "";
            }
        });

        observer.observe(resultsContainer, {
            attributes: true,
            attributeFilter: ["class"]
        });
    }

    /* Feedback visuel au clic sur les boutons principaux */
    document.querySelectorAll(".btn-primary").forEach((button) => {
        button.addEventListener("click", () => {
            if (reduceMotion) return;

            button.animate(
                [
                    { transform: "scale(1)" },
                    { transform: "scale(.97)" },
                    { transform: "scale(1)" }
                ],
                {
                    duration: 220,
                    easing: "cubic-bezier(.34, 1.56, .64, 1)"
                }
            );
        });
    });

});