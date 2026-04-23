# 🧪 Testing Authentication - Jalon 2.1

## Setup

```bash
cd backend
docker-compose up -d   # Si Docker daemon est actif
# Ou en local:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://masroufi_dev:masroufi_dev_password@localhost:5432/masroufi_db
```

## Tester via Swagger

Accédez à : `http://localhost:8000/docs`

Tous les endpoints d'authentification sont documentés avec essai interactif.

## Tester via cURL

### 1. Health Checks

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
```

### 2. Signup

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "name": "John Doe"
  }'

# Réponse attendue :
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "is_active": true,
    "created_at": "2025-04-23T..."
  }
}
```

### 3. Login

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }' | jq -r '.access_token')

echo "Access Token: $TOKEN"
```

### 4. Get Current User

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Refresh Token

```bash
REFRESH_TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }' | jq -r '.refresh_token')

curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}"
```

### 6. Update User Profile

```bash
curl -X PUT http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "password": "newpassword123"
  }'
```

## Validations à tester

### ✅ Email validation
- Email invalide → 422 Unprocessable Entity
- Email déjà enregistré → 400 Bad Request

### ✅ Password validation
- Mot de passe < 8 caractères → 422 Unprocessable Entity
- Mauvais mot de passe au login → 401 Unauthorized

### ✅ Token validation
- Token invalide → 401 Unauthorized
- Token expiré → 401 Unauthorized (after 24h pour access token)
- Refresh token valide → nouveau access token

### ✅ User state
- User inactif (is_active=False) → 403 Forbidden

## Base de données

Vérifier que l'utilisateur est créé :

```bash
docker exec masroufi-db-1 psql -U masroufi_dev -d masroufi_db -c "SELECT * FROM users;"
```

## Notes

- Les tokens JWT expirent après **24 heures** (access) et **7 jours** (refresh)
- Les mots de passe sont hashés avec bcrypt
- Les timestamps sont en UTC (datetime.utcnow())
- Chaque utilisateur a un UUID unique
