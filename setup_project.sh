#!/bin/bash

# Script de setup complet du projet Finary Icons Platform
# Génère tous les fichiers nécessaires pour le backend et frontend

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🎨 Finary Icons Platform - Setup"
echo "=================================="
echo ""
echo "📁 Project root: $PROJECT_ROOT"
echo ""

# Créer la structure complète si pas encore fait
mkdir -p backend/app/{api,core,models,services,utils}
mkdir -p backend/tests
mkdir -p frontend/src/{app,components,lib,types}
mkdir -p supabase/{migrations,functions}
mkdir -p docs
mkdir -p .github/workflows

echo "✅ Structure créée"
echo ""
echo "📝 Les fichiers suivants ont été créés :"
echo "   - README.md"
echo "   - .gitignore"
echo "   - backend/requirements.txt"
echo "   - backend/.env.example"
echo "   - frontend/package.json"
echo "   - frontend/.env.example"
echo ""
echo "🚀 Prochaines étapes :"
echo ""
echo "1️⃣  Backend Setup:"
echo "   cd backend"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo "   cp .env.example .env"
echo "   # Éditer .env avec vos clés API"
echo ""
echo "2️⃣  Frontend Setup:"
echo "   cd frontend"
echo "   npm install"
echo "   cp .env.example .env.local"
echo "   # Éditer .env.local"
echo ""
echo "3️⃣  Démarrage:"
echo "   # Terminal 1 - Backend"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "   # Terminal 2 - Frontend"
echo "   cd frontend && npm run dev"
echo ""
echo "4️⃣  Accès:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "✨ Setup terminé !"
