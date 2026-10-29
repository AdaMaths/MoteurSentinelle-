# Architecture Technique — MoteurSentinelle

## 1. Vue d'ensemble
MoteurSentinelle sépare strictement ses couches de responsabilités :
- **Frontend** : Application responsive en HTML5/CSS3/JS Vanilla. Conçue pour une exécution fluide même sur connexions 3G d'atelier.
- **Backend API & Diagnostic** : FastAPI (Python 3.11+) exposant un moteur de règles déterministe, explicable et non-probabiliste.
- **Persistance** : SQLite local en mode autonome/développement, convertible vers PostgreSQL et Directus CMS en environnement de production.

## 2. Déploiement Vercel vs Serveur Dédié
- **Frontend** : Déployable nativement et gratuitement sur Vercel.
- **Backend Python** : Exécutable sur Vercel Serverless Functions avec la contrainte suivante : Vercel réinitialise le système de fichiers `/tmp` à chaque démarrage à froid. En conséquence, **aucune base SQLite ne peut persister sur Vercel**. Une base PostgreSQL externe (ex. Neon, Supabase) est obligatoire en production cloud.
- En développement local ou sur serveur dédié (VPS / Docker), SQLite garantit la persistance immédiate sans coût d'infrastructure.
