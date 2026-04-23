# 🎨 Frontend Masroufi

React + TypeScript + Vite pour l'interface de Masroufi.

## Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Accédez à : `http://localhost:5173`

L'API est accessible via proxy (configure dans vite.config.ts)

## Structure

```
src/
├── api/           # Client Axios + fonctions API
├── components/    # Composants réutilisables
├── pages/         # Pages (Login, Dashboard, etc.)
├── hooks/         # Hooks React Query
├── context/       # Contextes (Auth, etc.)
├── types/         # Types TypeScript
├── utils/         # Utilitaires
└── styles/        # Styles globaux
```

## Jalons Implémentation

- ✅ 3.1 : Setup Vite + TS + dépendances
- 3.2 : Auth (Login/Signup)
- 3.3 : Dashboard
- 3.4 : Expenses & Categories CRUD
- 3.5 : Budgets
- 3.6 : Export
- 3.7 : Recurring & API tokens

## Dépendances principales

- **React 18** : UI framework
- **Vite** : Build tool rapide
- **React Query** : Gestion state serveur
- **Axios** : HTTP client avec intercepteurs JWT
- **Recharts** : Graphiques
- **React Router** : Navigation

## Development

```bash
npm run dev      # Démarrer dev server (HMR)
npm run build    # Build pour production
npm run preview  # Prévisualiser build
```

## Notes

- JWT tokens stockés dans localStorage
- Auto-refresh du token via interceptor Axios
- Proxy `/api` vers backend (8000)
