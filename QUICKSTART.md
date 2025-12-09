# 🚀 Quickstart - Finary Icons Platform

## 📦 État actuel du projet

✅ Structure créée
✅ Fichiers de configuration
✅ Git initialisé
✅ Premier commit effectué

## 🔗 Push sur GitHub

### 1️⃣ Créer le repo sur GitHub

1. Va sur https://github.com/new
2. Nom du repo : `finary-icons-platform`
3. Description : "Plateforme de génération d'icônes style Finary avec IA"
4. **Public** ou **Private** (ton choix)
5. ❌ **NE PAS** initialiser avec README (on en a déjà un)
6. Clique "Create repository"

### 2️⃣ Pusher le code

```bash
cd ~/Desktop/finary-icons-platform

# Ajouter le remote (remplace 'ton-username' par ton username GitHub)
git remote add origin https://github.com/ton-username/finary-icons-platform.git

# Push
git branch -M main
git push -u origin main
```

### 3️⃣ Vérifier

Ouvre https://github.com/ton-username/finary-icons-platform

Tu devrais voir tous les fichiers !

---

## 🏃 Démarrage rapide du projet

### Backend

```bash
cd ~/Desktop/finary-icons-platform/backend

# Environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec tes clés API

# Démarrer
uvicorn app.main:app --reload
```

API disponible sur http://localhost:8000
Documentation auto sur http://localhost:8000/docs

### Frontend

```bash
cd ~/Desktop/finary-icons-platform/frontend

# Installer les dépendances
npm install

# Configurer les variables d'environnement
cp .env.example .env.local
# Éditer .env.local

# Démarrer
npm run dev
```

Interface web sur http://localhost:3000

---

## 🔑 Clés API nécessaires

### Pour démarrer (minimum)

- `GEMINI_API_KEY` - Génération d'images (Nano Banana Pro)
  - Obtenir : https://aistudio.google.com/app/apikey

- `SUPABASE_URL` + `SUPABASE_ANON_KEY` - Base de données
  - Obtenir : https://supabase.com (créer un projet gratuit)

### Optionnel (pour fonctionnalités avancées)

- `OPENAI_API_KEY` - Extraction de concepts YouTube
- `REPLICATE_API_TOKEN` - Détourage BRIA RMBG 2.0

---

## 📁 Structure du projet

```
finary-icons-platform/
├── README.md              # Documentation principale
├── QUICKSTART.md          # Ce fichier
├── setup_project.sh       # Script de setup automatique
├── .gitignore
│
├── backend/               # API FastAPI
│   ├── app/
│   │   ├── api/          # Routes API
│   │   ├── core/         # Configuration
│   │   ├── models/       # Modèles de données
│   │   ├── services/     # Services (IA, Supabase)
│   │   └── utils/        # Utilitaires
│   ├── tests/            # Tests
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/             # Interface Next.js
│   ├── src/
│   │   ├── app/         # Pages (App Router)
│   │   ├── components/  # Composants React
│   │   ├── lib/         # Librairies
│   │   └── types/       # Types TypeScript
│   ├── public/          # Fichiers statiques
│   ├── package.json
│   └── .env.example
│
├── supabase/            # Configuration Supabase
│   ├── migrations/      # Migrations SQL
│   └── functions/       # Edge Functions
│
└── docs/                # Documentation
    ├── ARCHITECTURE.md
    ├── API.md
    └── DEPLOYMENT.md
```

---

## ✨ Prochaines étapes

1. ✅ Créer le repo GitHub et pusher
2. ⏳ Compléter le code backend (API endpoints)
3. ⏳ Compléter le code frontend (UI)
4. ⏳ Configurer Supabase
5. ⏳ Déployer sur Vercel

---

## 💡 Commandes utiles

### Git

```bash
# Status
git status

# Add + Commit + Push
git add .
git commit -m "Description des changements"
git push

# Voir l'historique
git log --oneline
```

### Backend

```bash
# Activer venv
source backend/venv/bin/activate

# Démarrer en mode dev
cd backend && uvicorn app.main:app --reload

# Tests
cd backend && pytest

# Installer une nouvelle dépendance
pip install nom-package
pip freeze > requirements.txt
```

### Frontend

```bash
# Démarrer en mode dev
cd frontend && npm run dev

# Build production
npm run build

# Linter
npm run lint

# Installer une nouvelle dépendance
npm install nom-package
```

---

## 🆘 Problèmes courants

### "No module named 'app'"

```bash
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "Cannot find module 'next'"

```bash
cd frontend
rm -rf node_modules
npm install
```

### Port déjà utilisé

```bash
# Backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (port 3000)
lsof -ti:3000 | xargs kill -9
```

---

**Questions ? Ouvre une issue sur GitHub !** 🎨
