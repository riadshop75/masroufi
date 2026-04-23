# 📦 Migrations Alembic - Masroufi

## Overview

Alembic gère les migrations de schéma PostgreSQL. Les modèles SQLAlchemy dans `app/models/` définissent la structure.

## Commandes essentielles

### Créer la BDD initiale

```bash
cd backend
export DATABASE_URL="postgresql://masroufi_dev:masroufi_dev_password@localhost:5432/masroufi_db"
alembic upgrade head
```

### Vérifier l'état des migrations

```bash
alembic current
alembic history
```

### Créer une nouvelle migration (après modification des modèles)

```bash
# Modifier les fichiers app/models/
alembic revision --autogenerate -m "Description de la migration"
# Cela génère un nouveau fichier dans alembic/versions/

# Vérifier la migration avant d'appliquer
cat alembic/versions/XXX_description.py

# Appliquer la migration
alembic upgrade head
```

### Annuler une migration

```bash
alembic downgrade -1  # revenir à la migration précédente
```

## Structure

- `alembic/env.py` : Configuration Alembic (lit DATABASE_URL depuis .env)
- `alembic/versions/` : Migrations historiques
- `alembic/script.py.mako` : Template pour nouvelles migrations
- `alembic.ini` : Configuration de base (peu modifié)

## Modèles (source de vérité)

Les modèles SQLAlchemy dans `app/models/` sont la source de vérité :
- `user.py` : Utilisateurs
- `category.py` : Catégories de dépenses
- `expense.py` : Dépenses individuelles
- `recurring_expense.py` : Dépenses récurrentes
- `budget.py` : Budgets par catégorie
- `api_token.py` : Tokens d'authentification API

## Workflow de développement

1. **Modifier un modèle** (ex: ajouter un champ)
   ```python
   # app/models/expense.py
   class Expense(Base):
       ...
       new_field = Column(String(255), nullable=True)
   ```

2. **Générer la migration**
   ```bash
   alembic revision --autogenerate -m "Add new_field to expenses"
   ```

3. **Vérifier la migration générée**
   ```bash
   cat alembic/versions/XXX_add_new_field_to_expenses.py
   # ⚠️ Alembic génère automatiquement, mais vérifiez toujours les détails
   ```

4. **Appliquer**
   ```bash
   alembic upgrade head
   ```

5. **Tester**
   ```bash
   psql -c "SELECT column_name FROM information_schema.columns WHERE table_name='expenses';"
   ```

## Notes importantes

- Toujours générer avant de modifier manuellement les migrations
- Les migrations sont cumulatives et irréversibles en production
- Le fichier `001_initial_schema.py` crée le schéma initial complet
- Utiliser `cascade="all, delete-orphan"` dans les relations pour les suppressions en cascade

## En cas de problème

### PostgreSQL rejette la migration

```bash
# Vérifier la connexion
psql -U masroufi_dev -d masroufi_db -c "SELECT version();"

# Vérifier l'état des migrations
alembic current

# Réinitialiser la BDD (dev only!)
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### Modèle vs schéma désynchronisé

```bash
# Régénérer une migration pour synchroniser
alembic revision --autogenerate -m "Sync models with schema"
alembic upgrade head
```
