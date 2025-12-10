"""
Test complet: Génération d'icônes + Upload Supabase
"""
import asyncio
import sys
import os
sys.path.insert(0, '/Users/tahina/Desktop/finary-icons-platform/backend')

from app.services.generation_service import generation_service
from app.services.supabase_service import supabase_service
from app.services.background_removal_service import background_removal_service
from dotenv import load_dotenv

load_dotenv()

async def test_full_flow():
    concepts = ["bitcoin", "ethereum", "stock market"]
    
    print("=" * 60)
    print("TEST COMPLET: Génération + Upload Supabase")
    print("=" * 60)
    print()
    
    for i, concept in enumerate(concepts, 1):
        try:
            print(f"[{i}/{len(concepts)}] Génération icône: {concept}...")
            
            # 1. Générer l'icône
            result = await generation_service.generate_icon(
                concept=concept,
                style="finary-glass-3d"
            )
            
            if not result or "image_data" not in result:
                print(f"  ❌ Échec génération pour {concept}")
                continue
            
            print(f"  ✅ Image générée ({len(result['image_data'])} chars base64)")
            
            # 2. Décoder base64 → bytes
            import base64
            image_bytes = base64.b64decode(result["image_data"])
            
            # 3. Supprimer l'arrière-plan
            print(f"  🔄 Suppression de l'arrière-plan...")
            clean_image = await background_removal_service.remove_background(image_bytes)
            
            if not clean_image:
                print(f"  ⚠️  Pas de nettoyage d'arrière-plan, utilisation de l'image originale")
                clean_image = image_bytes
            else:
                print(f"  ✅ Arrière-plan supprimé")
            
            # 4. Upload vers Supabase
            print(f"  🔄 Upload vers Supabase...")
            image_url = await supabase_service.upload_icon_image(
                image_data=clean_image,
                icon_name=concept
            )
            
            if not image_url:
                print(f"  ❌ Échec upload Supabase pour {concept}")
                continue
            
            print(f"  ✅ Upload réussi: {image_url[:80]}...")
            
            # 5. Créer l'entrée dans la base de données
            print(f"  🔄 Création entrée BDD...")
            icon_data = {
                "name": concept,
                "category": "crypto" if concept in ["bitcoin", "ethereum"] else "finance",
                "prompt": result["prompt"],
                "animation_prompt": result.get("animation_prompt", ""),
                "image_url": image_url,
                "metadata": {
                    "style": "finary-glass-3d",
                    "size": result.get("size", "2048x2048"),
                    "model": "gemini-3-pro-image-preview"
                }
            }
            
            icon_id = await supabase_service.create_icon(icon_data)
            
            if icon_id:
                print(f"  ✅ Icône créée avec ID: {icon_id}")
            else:
                print(f"  ❌ Échec création BDD pour {concept}")
            
            print()
            
        except Exception as e:
            print(f"  ❌ Erreur pour {concept}: {e}")
            print()
            continue
    
    print("=" * 60)
    print("✅ TEST TERMINÉ!")
    print("=" * 60)
    print()
    print("👉 Vérifie http://localhost:3000 pour voir les icônes!")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
