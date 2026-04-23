# Dépannage du Push Git - Masroufi

## Erreur Actuelle
```
Error 403: Permission to riadshop75/masroufi.git denied to riadshop75
```

## Causes Possibles

### 1. **L'utilisateur GitHub n'a pas les droits**
- L'utilisateur `riadshop75` n'est peut-être pas collaborateur du repo
- Ou n'a pas les permissions de push

### 2. **Token GitHub expiré ou invalide**
- Le proxy utilise un token qui n'est plus valide
- Besoin de régénérer le token GitHub

### 3. **Proxy Git non configuré correctement**
- Port: 37649 (actuellement actif)
- URL: `http://127.0.0.1:37649/git/riadshop75/masroufi`

## Solutions

### Solution 1: Vérifier les Permissions GitHub
1. Va sur https://github.com/riadshop75/masroufi
2. Vérifiez les settings → Collaborators
3. Assure-toi que `riadshop75` a les droits de push
4. Si non, ajoute-le comme collaborateur

### Solution 2: Régénérer le Token GitHub
1. Va sur GitHub Settings → Developer Settings → Personal Access Tokens
2. Crée un nouveau token avec scope `repo` complet
3. Mets à jour le proxy git avec ce token

### Solution 3: Utiliser un Autre Compte
Si `riadshop75` n'a pas accès, essaie avec un autre compte GitHub qui a les droits

## Commandes pour Pousser (une fois l'auth corrigée)

```bash
cd /home/user/masroufi

# Vérifier les commits en attente
git log origin/main..HEAD --oneline

# Pousser la branche
git push -u origin claude/review-project-docs-fPQlM

# Ou, si tu veux pousser vers main directement
git push -u origin claude/review-project-docs-fPQlM:main
```

## Commits en Attente (10 total)

| SHA | Message |
|-----|---------|
| 97caaec | Ajouter guide complet de localisation du code |
| b1b4010 | Ajouter backups/patches au gitignore |
| 05ebac0 | ✅ FINAL : Masroufi 100% implémenté (14/14 jalons) |
| 2893fb3 | Jalons 3.2-3.7 : Frontend React complet (8 pages) |
| 2fe9388 | Ajouter résumé complet d'implémentation (9/14 jalons) |
| bab0676 | Jalon 3.1 : Setup React + Vite + Infrastructure |
| c4bdf8d | Jalons 2.2-2.7 : Backend complet |
| 99b3250 | Jalon 2.1 : Setup FastAPI + Authentification JWT |
| 4e740f6 | Jalon 1.2 : Modèle de données & migrations |
| 6b53be8 | Jalon 1.1 : Infrastructure Docker & PostgreSQL |

## Sauvegarde des Commits

Les commits ont été sauvegardés dans:
- **Bundle Git**: `masroufi-commits.bundle` (101 KB)
- **Patches**: `/tmp/patches/0001-*.patch` (10 fichiers)

### Restaurer depuis le Bundle
```bash
git bundle verify masroufi-commits.bundle
git pull masroufi-commits.bundle
```

### Restaurer depuis les Patches
```bash
git am /tmp/patches/*.patch
```

## Chemin du Projet
- **Sur Linux/WSL**: `/home/user/masroufi`
- **Sur Windows**: À déterminer selon la configuration de Claude Code

## Contact Support
Si le problème persiste:
1. Vérifie la configuration du proxy git dans Claude Code settings
2. Redémarre Claude Code
3. Réessaie le push avec les bonnes authentifications
