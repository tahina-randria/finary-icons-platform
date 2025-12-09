# 🎨 Finary Icons Platform

> Plateforme complète de génération et gestion d'icônes style Finary avec IA

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)

## 📋 Vue d'ensemble

Système automatisé de génération d'icônes depuis des transcriptions YouTube ou concepts manuels, avec détourage IA et interface web pour les monteurs/motion designers.

### 🎯 Fonctionnalités

- ✅ **Extraction intelligente de concepts** depuis YouTube (tous types : finance, objets, lieux, métiers...)
- ✅ **Génération d'icônes IA** avec Nano Banana Pro (Gemini 3 Pro Image)
- ✅ **Détourage state-of-the-art** avec BRIA RMBG 2.0
- ✅ **Interface web** pour recherche, génération et téléchargement
- ✅ **API REST complète** avec FastAPI
- ✅ **Base de données** Supabase (PostgreSQL + Storage)

## 🚀 Stack Technique

### Backend
- **FastAPI** - API REST haute performance
- **Nano Banana Pro** (Gemini 3 Pro Image) - Génération d'images
- **BRIA RMBG 2.0** - Détourage IA
- **OpenAI GPT-4** - Extraction de concepts
- **Supabase** - Base de données + Storage

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Typage statique
- **Tailwind CSS** - Styling
- **shadcn/ui** - Composants UI

### Infra
- **Vercel** - Hébergement frontend
- **Vercel Serverless** - Backend API
- **Supabase** - Database + Storage + Auth

## 📦 Installation

### Prérequis

```bash
# Node.js 18+
node --version

# Python 3.9+
python3 --version

# Git
git --version
```

### Clone du projet

```bash
git clone https://github.com/votre-username/finary-icons-platform.git
cd finary-icons-platform
```

### Configuration Backend

```bash
cd backend

# Environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Dépendances
pip install -r requirements.txt

# Variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API
```

### Configuration Frontend

```bash
cd frontend

# Dépendances
npm install

# Variables d'environnement
cp .env.example .env.local
# Éditer .env.local
```

## 🔑 Variables d'environnement

### Backend `.env`

```bash
# API Keys
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
REPLICATE_API_TOKEN=...

# Supabase
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_KEY=...

# Optional
YOUTUBE_API_KEY=...
```

### Frontend `.env.local`

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

## 🏃 Démarrage

### Backend (développement)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

API disponible sur `http://localhost:8000`
Documentation auto : `http://localhost:8000/docs`

### Frontend (développement)

```bash
cd frontend
npm run dev
```

Interface web sur `http://localhost:3000`

## 📖 Documentation

- [Architecture](./docs/ARCHITECTURE.md)
- [API Documentation](./docs/API.md)
- [Déploiement](./docs/DEPLOYMENT.md)
- [Contribution](./docs/CONTRIBUTING.md)

## 🎯 Workflow

```
📹 YouTube URL
    ↓
📝 Extraction transcription
    ↓
🤖 Analyse IA (GPT-4) → Concepts
    ↓
✨ Génération (Nano Banana Pro)
    ↓
🪄 Détourage (BRIA RMBG 2.0)
    ↓
☁️ Upload Supabase Storage
    ↓
🌐 Disponible dans l'interface web
```

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (Next.js)                     │
│  - Recherche d'icônes                   │
│  - Génération à la demande              │
│  - Téléchargements batch                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Backend API (FastAPI)                  │
│  - Endpoints REST                       │
│  - Services IA                          │
│  - Queue génération                     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Supabase                               │
│  - PostgreSQL (métadonnées)             │
│  - Storage (images PNG)                 │
│  - Auth (utilisateurs)                  │
└─────────────────────────────────────────┘
```

## 💰 Coûts

### Par icône générée

- Nano Banana Pro : **$0.12** (2K)
- BRIA RMBG 2.0 : **Gratuit** (open-source)
- **Total** : ~$0.12 par icône

### Hébergement (mensuel)

- Supabase Free : **$0**
- Vercel Free : **$0**
- **Total démarrage** : $0 + coût génération

### Production

- Supabase Pro : **$25/mois**
- Vercel Pro : **$20/mois**
- Génération (50 icônes/mois) : **$6/mois**
- **Total** : ~$50/mois

## 🚀 Déploiement

### Vercel (Frontend + Backend)

```bash
# Installer Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

cd ../backend
vercel
```

### Supabase

1. Créer un projet sur [supabase.com](https://supabase.com)
2. Exécuter les migrations SQL
3. Configurer Storage buckets
4. Copier les clés dans `.env`

Voir [DEPLOYMENT.md](./docs/DEPLOYMENT.md) pour détails complets.

## 🧪 Tests

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

## 📝 Exemples d'utilisation

### Générer depuis YouTube

```bash
curl -X POST http://localhost:8000/api/generate/youtube \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=..."}'
```

### Rechercher des icônes

```bash
curl http://localhost:8000/api/icons/search?q=bitcoin
```

### Télécharger une icône

```bash
curl http://localhost:8000/api/download/{icon_id}/2k \
  -o bitcoin_2k.png
```

## 🤝 Contribution

Les contributions sont bienvenues ! Voir [CONTRIBUTING.md](./docs/CONTRIBUTING.md).

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

## 📄 License

MIT License - voir [LICENSE](LICENSE)

## 🙏 Remerciements

- [Nano Banana Pro](https://ai.google.dev/gemini-api/docs/imagen) - Génération d'images
- [BRIA RMBG 2.0](https://huggingface.co/briaai/RMBG-2.0) - Détourage
- [Supabase](https://supabase.com) - Backend as a Service
- [Vercel](https://vercel.com) - Hébergement

## 📞 Support

- 📧 Email: support@finary-icons.com
- 💬 Discord: [Rejoindre](https://discord.gg/...)
- 📖 Docs: [docs.finary-icons.com](https://docs.finary-icons.com)

---

**Made with ❤️ for Finary monteurs & motion designers**
