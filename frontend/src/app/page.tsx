'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import type { Icon } from '@/types/icon';

export default function Home() {
  const [icons, setIcons] = useState<Icon[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadIcons();
  }, []);

  const loadIcons = async () => {
    try {
      setLoading(true);
      const result = await api.listIcons({ page: 1, page_size: 12 });
      setIcons(result.icons);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load icons');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-slate-900 mb-4">
          Finary Icons Platform
        </h1>
        <p className="text-xl text-slate-600 mb-8">
          Génération d'icônes IA pour vos vidéos d'analyse patrimoniale
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/generate"
            className="px-6 py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            Générer des icônes
          </a>
          <a
            href="/icons"
            className="px-6 py-3 border border-slate-300 rounded-lg hover:border-slate-400 transition-colors"
          >
            Parcourir la bibliothèque
          </a>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
        <div className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">YouTube → Icônes</h3>
          <p className="text-slate-600">
            Extrayez automatiquement les concepts d'une vidéo YouTube et générez les icônes correspondantes
          </p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">IA Avancée</h3>
          <p className="text-slate-600">
            Gemini 3 Pro Image + BRIA RMBG 2.0 pour des icônes de qualité professionnelle
          </p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Style Finary</h3>
          <p className="text-slate-600">
            Icônes 3D glass morphism, sans reflet au sol, optimisées pour le motion design
          </p>
        </div>
      </div>

      {/* Recent Icons */}
      <div>
        <h2 className="text-3xl font-bold text-slate-900 mb-8">
          Icônes récentes
        </h2>

        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-slate-900"></div>
            <p className="mt-4 text-slate-600">Chargement...</p>
          </div>
        )}

        {error && (
          <div className="text-center py-12">
            <p className="text-red-600">{error}</p>
            <button
              onClick={loadIcons}
              className="mt-4 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800"
            >
              Réessayer
            </button>
          </div>
        )}

        {!loading && !error && icons.length === 0 && (
          <div className="text-center py-12">
            <p className="text-slate-600 mb-4">
              Aucune icône disponible pour le moment
            </p>
            <a
              href="/generate"
              className="px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 inline-block"
            >
              Créer votre première icône
            </a>
          </div>
        )}

        {!loading && !error && icons.length > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
            {icons.map((icon) => (
              <a
                key={icon.id}
                href={`/icons/${icon.id}`}
                className="group bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="aspect-square bg-slate-100 rounded-lg mb-3 flex items-center justify-center overflow-hidden">
                  <img
                    src={icon.thumbnail_url || icon.image_url}
                    alt={icon.name}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform"
                  />
                </div>
                <p className="text-sm font-medium text-slate-900 truncate">
                  {icon.name}
                </p>
                <p className="text-xs text-slate-500 capitalize">
                  {icon.category.replace(/_/g, ' ')}
                </p>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
