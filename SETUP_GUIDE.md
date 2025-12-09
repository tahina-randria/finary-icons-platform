# 🚀 Guide de Setup - Finary Icons Platform

## Étape par Étape pour Démarrer

### ✅ Prérequis
- Python 3.9+ installé ✓
- Node.js 18+ (à installer si besoin)
- Compte GitHub ✓

---

## 📋 Checklist Rapide

### 1️⃣ Supabase (Base de données) - GRATUIT

**a) Créer le projet:**
- Va sur https://supabase.com
- Login avec GitHub
- "New project" → Nom: `finary-icons`
- Region: Europe West
- Plan: Free (gratuit)
- **Sauvegarde le Database Password!**

**b) Récupérer les clés API:**
- Va dans **Settings** (⚙️) → **API**
- Copie:
  - `Project URL` (ex: https://abc123.supabase.co)
  - `anon public` key (commence par eyJ...)
  - `service_role` key (commence par eyJ... aussi)

**c) Configurer la base de données:**
- Va dans **SQL Editor** (dans le menu)
- Clique "New query"
- Copie/colle TOUT le contenu de `supabase/migrations/001_initial_schema.sql`
- Clique "Run"
- Ensuite, copie/colle `supabase/migrations/002_storage_setup.sql`
- Clique "Run"

✅ Database prête!

---

### 2️⃣ Gemini API Key (Génération d'images) - GRATUIT

- Va sur https://aistudio.google.com/app/apikey
- Login avec Google
- "Create API Key" → "Create API key in new project"
- Copie la clé (commence par AIza...)

✅ Clé Gemini obtenue!

---

### 3️⃣ Configuration Backend

**Éditer** `backend/.env` et remplacer:
```bash
# Remplace ces valeurs avec celles de Supabase
SUPABASE_URL=https://TON-PROJECT.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# Remplace avec ta clé Gemini
GEMINI_API_KEY=AIza...
```

---

### 4️⃣ Configuration Frontend

**Éditer** `frontend/.env.local` et remplacer:
```bash
# Mêmes valeurs que backend
NEXT_PUBLIC_SUPABASE_URL=https://TON-PROJECT.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

---

### 5️⃣ Installer les dépendances

**Backend:**
```bash
cd ~/Desktop/finary-icons-platform/backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd ~/Desktop/finary-icons-platform/frontend
npm install
```

---

### 6️⃣ Démarrer les serveurs

**Terminal 1 - Backend:**
```bash
cd ~/Desktop/finary-icons-platform/backend
source venv/bin/activate
python3 -m uvicorn app.main:app --reload
```

Ouvre http://localhost:8000/docs pour voir l'API!

**Terminal 2 - Frontend:**
```bash
cd ~/Desktop/finary-icons-platform/frontend
npm run dev
```

Ouvre http://localhost:3000 pour voir l'interface!

---

## 🎯 Test Rapide

1. Ouvre http://localhost:3000
2. Clique "Générer des icônes"
3. Onglet "À partir d'un concept"
4. Entre: "Bitcoin"
5. Clique "Générer l'icône"
6. Attends... Une icône devrait être générée!

---

## ⚠️ Troubleshooting

### Port 8000 déjà utilisé
```bash
lsof -ti:8000 | xargs kill -9
```

### Port 3000 déjà utilisé
```bash
lsof -ti:3000 | xargs kill -9
```

### Module not found (Backend)
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Cannot find module (Frontend)
```bash
cd frontend
rm -rf node_modules
npm install
```

---

## 🔑 Clés API Optionnelles (pour + de fonctionnalités)

### OpenAI (pour extraction YouTube)
- https://platform.openai.com/api-keys
- Ajoute dans `backend/.env`: `OPENAI_API_KEY=sk-...`

### Replicate (pour détourage BRIA)
- https://replicate.com/account/api-tokens
- Ajoute dans `backend/.env`: `REPLICATE_API_TOKEN=r8_...`

---

## 📚 Documentation

- **README.md** - Vue d'ensemble complète
- **QUICKSTART.md** - Guide rapide
- **IMPLEMENTATION_COMPLETE.md** - Détails techniques

---

## 🆘 Besoin d'aide?

Si tu bloques quelque part, dis-moi à quelle étape et je t'aide!
