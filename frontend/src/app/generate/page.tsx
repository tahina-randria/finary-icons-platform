'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { isValidYouTubeUrl } from '@/lib/utils';
import type { GenerationTask } from '@/types/icon';

export default function GeneratePage() {
  const [tab, setTab] = useState<'concept' | 'youtube'>('concept');
  const [concept, setConcept] = useState('');
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [task, setTask] = useState<GenerationTask | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateConcept = async () => {
    if (!concept.trim()) {
      setError('Veuillez entrer un concept');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await api.generateFromConcept({ concept });

      // Poll for status
      const finalTask = await api.pollGenerationStatus(
        response.task_id,
        (task) => setTask(task)
      );

      setTask(finalTask);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Échec de la génération');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateYouTube = async () => {
    if (!youtubeUrl.trim()) {
      setError('Veuillez entrer une URL YouTube');
      return;
    }

    if (!isValidYouTubeUrl(youtubeUrl)) {
      setError('URL YouTube invalide');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await api.generateFromYouTube({ youtube_url: youtubeUrl });

      // Poll for status
      const finalTask = await api.pollGenerationStatus(
        response.task_id,
        (task) => setTask(task)
      );

      setTask(finalTask);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Échec de la génération');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <h1 className="text-4xl font-bold text-slate-900 mb-8">
        Générer des icônes
      </h1>

      {/* Tabs */}
      <div className="flex gap-4 mb-8 border-b">
        <button
          onClick={() => setTab('concept')}
          className={`px-4 py-2 font-medium transition-colors ${
            tab === 'concept'
              ? 'text-slate-900 border-b-2 border-slate-900'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          À partir d'un concept
        </button>
        <button
          onClick={() => setTab('youtube')}
          className={`px-4 py-2 font-medium transition-colors ${
            tab === 'youtube'
              ? 'text-slate-900 border-b-2 border-slate-900'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          À partir de YouTube
        </button>
      </div>

      {/* Concept Tab */}
      {tab === 'concept' && (
        <div className="bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-xl font-semibold mb-4">Générer depuis un concept</h2>
          <p className="text-slate-600 mb-6">
            Entrez un concept et nous générerons une icône style Finary
          </p>

          <div className="mb-6">
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Concept
            </label>
            <input
              type="text"
              value={concept}
              onChange={(e) => setConcept(e.target.value)}
              placeholder="Ex: Bitcoin, Investissement immobilier, Épargne..."
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900"
              disabled={loading}
            />
          </div>

          <button
            onClick={handleGenerateConcept}
            disabled={loading || !concept.trim()}
            className="w-full px-6 py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Génération en cours...' : 'Générer l\'icône'}
          </button>
        </div>
      )}

      {/* YouTube Tab */}
      {tab === 'youtube' && (
        <div className="bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-xl font-semibold mb-4">Générer depuis YouTube</h2>
          <p className="text-slate-600 mb-6">
            Entrez l'URL d'une vidéo YouTube. Nous extrairons automatiquement les concepts et générerons les icônes correspondantes.
          </p>

          <div className="mb-6">
            <label className="block text-sm font-medium text-slate-700 mb-2">
              URL YouTube
            </label>
            <input
              type="url"
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900"
              disabled={loading}
            />
          </div>

          <button
            onClick={handleGenerateYouTube}
            disabled={loading || !youtubeUrl.trim()}
            className="w-full px-6 py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Extraction et génération...' : 'Extraire et générer'}
          </button>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Task Status */}
      {task && (
        <div className="mt-8 bg-white rounded-lg shadow-sm p-8">
          <h3 className="text-lg font-semibold mb-4">État de la génération</h3>

          <div className="mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-slate-600">Progression</span>
              <span className="font-medium">{task.progress}%</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
              <div
                className="bg-slate-900 h-2 rounded-full transition-all duration-300"
                style={{ width: `${task.progress}%` }}
              />
            </div>
          </div>

          <div className="space-y-2">
            <p className="text-sm">
              <span className="font-medium">Statut:</span>{' '}
              <span className="capitalize">{task.status.replace(/_/g, ' ')}</span>
            </p>
            {task.message && (
              <p className="text-sm text-slate-600">{task.message}</p>
            )}
            {task.generated_icons && task.generated_icons.length > 0 && (
              <div>
                <p className="text-sm font-medium mb-2">
                  Icônes générées: {task.generated_icons.length}
                </p>
                <a
                  href="/icons"
                  className="text-sm text-slate-900 underline hover:no-underline"
                >
                  Voir mes icônes
                </a>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
