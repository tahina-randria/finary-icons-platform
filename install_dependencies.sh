#!/bin/bash

echo "🎨 Finary Icons Platform - Installation des dépendances"
echo "========================================================="
echo ""

# Backend
echo "📦 Installation des dépendances Backend..."
cd ~/Desktop/finary-icons-platform/backend

if [ ! -d "venv" ]; then
    echo "  → Création de l'environnement virtuel Python..."
    python3 -m venv venv
fi

echo "  → Activation de l'environnement virtuel..."
source venv/bin/activate

echo "  → Installation des packages Python..."
pip install --upgrade pip > /dev/null 2>&1
pip install fastapi uvicorn pydantic-settings loguru supabase httpx python-dotenv --user

echo "  ✅ Backend prêt!"
echo ""

# Frontend
echo "📦 Installation des dépendances Frontend..."
cd ~/Desktop/finary-icons-platform/frontend

echo "  → Installation des packages npm..."
npm install

echo "  ✅ Frontend prêt!"
echo ""

echo "========================================================="
echo "✅ Installation terminée!"
echo ""
echo "📝 Prochaines étapes:"
echo "  1. Configure backend/.env avec tes clés API"
echo "  2. Configure frontend/.env.local avec Supabase"
echo "  3. Exécute les migrations Supabase (voir SETUP_GUIDE.md)"
echo ""
echo "🚀 Pour démarrer:"
echo "  Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo ""
