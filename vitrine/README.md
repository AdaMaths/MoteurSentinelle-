# Site vitrine MoteurSentinelle Pro

Site public indépendant de l'application de diagnostic. Il est placé dans `vitrine/` afin de ne pas modifier le frontend existant situé dans `frontend/`.

## Déploiement Vercel

Créer un nouveau projet Vercel depuis le dépôt `AdaMaths/MoteurSentinelle-` :

- Branch : `seo-vitrine` pour le premier déploiement de validation (ou `main` après fusion de la branche).
- Root Directory : `vitrine`
- Framework Preset : Other
- Build Command : laisser vide
- Output Directory : `.`

Après le déploiement, relever le vrai domaine attribué par Vercel et remplacer partout dans les fichiers HTML, `robots.txt` et `sitemap.xml` le domaine provisoire `moteur-sentinelle-vitrine.vercel.app` par ce domaine réel. Vérifier aussi l'URL canonique et l'image Open Graph.

## SEO après déploiement

1. Vérifier que la page d'accueil et les pages HTML répondent en HTTPS.
2. Vérifier `/robots.txt` et `/sitemap.xml`.
3. Ajouter le domaine dans Google Search Console et valider la propriété.
4. Soumettre le sitemap et demander l'indexation des pages publiques.
5. Contrôler les résultats d'indexation et les éventuels problèmes dans Search Console.

Le site ne collecte aucun formulaire et ne publie aucune coordonnée personnelle. La présentation décrit les fonctionnalités documentées dans l'application et rappelle que les résultats sont une aide à la décision, pas un diagnostic certifié.
