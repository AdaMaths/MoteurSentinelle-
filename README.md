# MoteurSentinelle ⚡

**Innovation numérique appliquée à la maintenance industrielle & au diagnostic électromécanique.**  
Conçu pour l'Afrique francophone (Sénégal) — Candidature au **Master Innovation Challenge (MIC) 2026**.

---

## 🚀 Démarrage rapide dans PyCharm

### 1. Ouvrir le projet
- Dans PyCharm : `File > Open...`
- Sélectionnez le dossier `moteursentinelle` sur votre Bureau.

### 2. Configurer l'environnement Python
- `File > Settings > Project: moteursentinelle > Python Interpreter`
- Ajoutez un interpréteur Python 3.11+ (Virtualenv).
- Faites un clic droit sur le dossier `backend` > **Mark Directory as > Sources Root**.

### 3. Installer les dépendances
Ouvrez le terminal en bas de PyCharm (`Alt + F12`) :
```bash
pip install -r backend/requirements.txt
```

### 4. Lancer les tests automatisés
```bash
pytest backend/tests/
```

### 5. Démarrer l'API Backend
```bash
python backend/app.py
```
L'API démarre sur `http://127.0.0.1:8000`. Vous pouvez tester la documentation Swagger sur `http://127.0.0.1:8000/docs`.

### 6. Ouvrir l'application Web
Faites un clic droit sur `frontend/index.html` > **Open in > Browser > Chrome / Edge**.

### 7. Démarrer Directus en local (optionnel)
Installez et démarrez Docker Desktop, puis créez `.env.directus` à partir de `.env.directus.example`. Remplacez les valeurs de démonstration par des secrets uniques avant de démarrer les services :
```powershell
Copy-Item .env.directus.example .env.directus
docker compose --env-file .env.directus -f directus/docker-compose.yml up -d
```
Ouvrez `http://localhost:8055` et connectez-vous avec l'adresse et le mot de passe définis dans `.env.directus`. Pour arrêter Directus :
```powershell
docker compose --env-file .env.directus -f directus/docker-compose.yml down
```
Ne publiez jamais `.env.directus` : ce fichier contient les mots de passe et les clés secrètes locaux.

---

## 📂 Architecture du Projet
- `backend/` : API FastAPI, moteur de règles électromécaniques déterministe, simulateur pédagogique, persistance SQLite.
- `frontend/` : Interface responsive en français (HTML5/CSS3/JS Vanilla), adaptée aux connexions mobiles d'atelier.
- `docs/mic2026/` : Dossier complet pour le Master Innovation Challenge (Présentation, Résumé 172 mots, Pitch 7 min, 15 Questions/Réponses, Roadmap).
- `directus/` : Modèle de données et fichier `docker-compose.yml` pour le déploiement Directus + PostgreSQL.
