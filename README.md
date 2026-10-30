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

### 7. Configurer Firebase Firestore (production, optionnel)
1. Créez un projet Firebase et activez une base de données Cloud Firestore.
2. Créez un compte de service avec les permissions minimales nécessaires, téléchargez sa clé JSON et placez-la dans `backend/firebase-service-account.json`. Ne publiez ni ne partagez jamais cette clé.
3. Créez `.env` à partir de `.env.example`, définissez `DATABASE_TYPE=firestore` et votre `FIREBASE_PROJECT_ID`. Placez la clé JSON du compte de service dans `backend/firebase-service-account.json` (chemin indiqué par `GOOGLE_APPLICATION_CREDENTIALS`).
4. Mettez à jour les dépendances et démarrez l'API :
   ```powershell
   pip install -r backend/requirements.txt
   python backend/app.py
   ```
En déploiement, configurez `DATABASE_TYPE=firestore`, `FIREBASE_PROJECT_ID` et `FIREBASE_SERVICE_ACCOUNT_JSON` (le contenu JSON de la clé) comme variables secrètes de la plateforme. Ne publiez jamais cette clé. Sans `DATABASE_TYPE=firestore`, l'application conserve SQLite en local.

---

## 📂 Architecture du Projet
- `backend/` : API FastAPI, moteur de règles électromécaniques déterministe, simulateur pédagogique, persistance SQLite locale ou Firebase Firestore.
- `frontend/` : Interface responsive en français (HTML5/CSS3/JS Vanilla), adaptée aux connexions mobiles d'atelier.
- `docs/mic2026/` : Dossier complet pour le Master Innovation Challenge (Présentation, Résumé 172 mots, Pitch 7 min, 15 Questions/Réponses, Roadmap).
