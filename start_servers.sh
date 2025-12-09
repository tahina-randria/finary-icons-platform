#!/bin/bash

echo "🚀 Démarrage de Finary Icons Platform"
echo "======================================"
echo ""

# Tuer les anciens processus
pkill -f "uvicorn app.main" 2>/dev/null
pkill -f "next dev" 2>/dev/null
sleep 1

# Démarrer le backend
echo "📦 Démarrage du backend..."
cd ~/Desktop/finary-icons-platform/backend
source venv/bin/activate
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "  ✅ Backend démarré (PID: $BACKEND_PID)"
echo "  📍 API: http://localhost:8000"
echo "  📖 Docs: http://localhost:8000/docs"
echo ""

# Attendre que le backend soit prêt
echo "⏳ Attente du backend..."
sleep 3

# Tester le backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "  ✅ Backend opérationnel!"
else
    echo "  ⚠️  Backend non accessible (normal au premier démarrage)"
fi
echo ""

# Démarrer le frontend
echo "🎨 Démarrage du frontend..."
cd ~/Desktop/finary-icons-platform/frontend
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  ✅ Frontend démarré (PID: $FRONTEND_PID)"
echo "  📍 Interface: http://localhost:3000"
echo ""

echo "======================================"
echo "✅ Serveurs démarrés!"
echo ""
echo "📝 Pour arrêter:"
echo "  pkill -f uvicorn"
echo "  pkill -f 'next dev'"
echo ""
echo "📋 Logs:"
echo "  Backend: tail -f ~/Desktop/finary-icons-platform/backend/backend.log"
echo "  Frontend: tail -f ~/Desktop/finary-icons-platform/frontend/frontend.log"
echo ""
echo "🌐 Ouvre http://localhost:3000 dans ton navigateur!"
