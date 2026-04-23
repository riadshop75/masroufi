# 🚀 Setup Masroufi - Phase d'Implémentation

## Jalon 1.1 : Infrastructure Docker & PostgreSQL ✅

### Prérequis
- Docker & Docker Compose (v20.10+)
- Git
- Node.js 16+ (pour frontend, plus tard)
- Python 3.11+ (optionnel si vous développez sans Docker)

### Démarrage rapide

1. **Cloner le repo et créer .env local**
```bash
cp .env.example .env
```

2. **Lancer l'infrastructure Docker**
```bash
docker-compose up -d
```

3. **Vérifier que tous les services sont actifs**
```bash
docker-compose ps
# Doit afficher : db (UP), app (UP), nginx (UP)
```

4. **Vérifier la connexion à PostgreSQL**
```bash
docker exec -it masroufi-db-1 psql -U masroufi_dev -d masroufi_db -c "\l"
# Doit afficher la liste des bases de données
```

5. **Vérifier l'API FastAPI**
```bash
curl http://localhost:8000/health
# Doit répondre : {"status":"ok"}

curl http://localhost:8000/api/v1/health
# Doit répondre : {"status":"ok","version":"1.0.0"}

# Consulter la documentation interactive
open http://localhost:8000/docs
```

### Arrêter l'infrastructure
```bash
docker-compose down
```

### Développement sans Docker (optionnel)

**Backend local :**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://masroufi_dev:masroufi_dev_password@localhost:5432/masroufi_db
uvicorn main:app --reload
```

### Troubleshooting

**Port 5432 déjà utilisé :**
```bash
# Changer le port dans docker-compose.yml ou arrêter le service local
docker-compose down
```

**Logs du conteneur app :**
```bash
docker-compose logs -f app
```

**Réinitialiser la base de données :**
```bash
docker-compose down -v
docker-compose up -d
```

---

## Prochaines étapes
- Jalon 1.2 : Modèle de données & migrations Alembic
