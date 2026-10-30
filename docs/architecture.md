# Architecture Technique — MoteurSentinelle

## 1. Vue d'ensemble
MoteurSentinelle sépare strictement ses couches de responsabilités :
- **Frontend** : Application responsive en HTML5/CSS3/JS Vanilla. Conçue pour une exécution fluide même sur connexions 3G d'atelier.
- **Backend API & Diagnostic** : FastAPI (Python 3.11+) exposant un moteur de règles déterministe, explicable et non-probabiliste.
- **Persistance** : SQLite local en mode autonome/développement ou Firebase Firestore en production, sélectionnés avec `DATABASE_TYPE`.

## 2. Déploiement Vercel vs Serveur Dédié
- **Frontend** : Déployable nativement et gratuitement sur Vercel.
- **Backend Python** : Exécutable sur Vercel Serverless Functions. Le système de fichiers n'étant pas persistant, utilisez Firebase Firestore (`DATABASE_TYPE=firestore`) plutôt que SQLite pour les données de production.
- En développement local ou sur serveur dédié (VPS / Docker), SQLite garantit la persistance immédiate sans coût d'infrastructure.
