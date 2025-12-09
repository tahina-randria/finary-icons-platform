'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { isValidYouTubeUrl } from '@/lib/utils';
import type { GenerationTask } from '@/types/icon';
import LoadingSpinner from '@/components/loading-spinner';

export default function GeneratePage() {
  const [tab, setTab] = useState<'concept' | 'youtube'>('concept');
  const [concept, setConcept] = useState('');
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [task, setTask] = useState<GenerationTask | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loadingMessage, setLoadingMessage] = useState('');

  const handleGenerateConcept = async () => {
    if (!concept.trim()) {
      setError('Veuillez entrer un concept');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setLoadingMessage('Création de la tâche de génération...');

      const response = await api.generateFromConcept({ concept });
      setLoadingMessage('Génération de l\'icône en cours...');

      // Poll for status
      const finalTask = await api.pollGenerationStatus(
        response.task_id,
        (task) => {
          setTask(task);
          // Update loading message based on status
          if (task.status === 'generating_images') {
            setLoadingMessage('Génération de l\'image avec Gemini...');
          } else if (task.status === 'removing_backgrounds') {
            setLoadingMessage('Détourage de l\'image...');
          } else if (task.status === 'uploading') {
            setLoadingMessage('Upload vers Supabase...');
          }
        }
      );

      setTask(finalTask);
      setLoadingMessage('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Échec de la génération');
      setLoadingMessage('');
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
      setLoadingMessage('Extraction de la transcription YouTube...');

      const response = await api.generateFromYouTube({ youtube_url: youtubeUrl });

      // Poll for status
      const finalTask = await api.pollGenerationStatus(
        response.task_id,
        (task) => {
          setTask(task);
          // Update loading message based on status
          if (task.status === 'extracting_concepts') {
            setLoadingMessage('Extraction des concepts avec GPT-4...');
          } else if (task.status === 'generating_images') {
            setLoadingMessage(`Génération des icônes (${task.generated_icons?.length || 0} créées)...`);
          } else if (task.status === 'removing_backgrounds') {
            setLoadingMessage('Détourage des images...');
          } else if (task.status === 'uploading') {
            setLoadingMessage('Upload vers Supabase...');
          }
        }
      );

      setTask(finalTask);
      setLoadingMessage('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Échec de la génération');
      setLoadingMessage('');
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

      {/* Loading Overlay */}
      {loading && (
        <div className="mt-8 space-y-6">
          <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg shadow-lg p-12">
            <div className="flex flex-col items-center space-y-6">
              <LoadingSpinner size="lg" />
              <div className="text-center space-y-2">
                <h3 className="text-xl font-semibold text-slate-900">
                  Génération en cours...
                </h3>
                {loadingMessage && (
                  <p className="text-slate-600 animate-pulse">{loadingMessage}</p>
                )}
                {task && (
                  <div className="mt-4 w-full max-w-md">
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-slate-600">Progression</span>
                      <span className="font-medium text-slate-900">{task.progress}%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-3 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-slate-600 to-slate-900 h-3 rounded-full transition-all duration-500 ease-out"
                        style={{ width: `${task.progress}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Transcript Display (YouTube only) */}
          {tab === 'youtube' && task?.transcript && task.transcript.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4 text-slate-900">
                📝 Transcription extraite ({task.transcript.length} segments)
              </h3>
              <div className="max-h-96 overflow-y-auto space-y-2 bg-slate-50 rounded-lg p-4">
                {task.transcript.map((segment, index) => {
                  const minutes = Math.floor(segment.start / 60);
                  const seconds = Math.floor(segment.start % 60);
                  const timestamp = `${minutes}:${seconds.toString().padStart(2, '0')}`;

                  return (
                    <div key={index} className="flex gap-3 text-sm border-b border-slate-200 pb-2">
                      <span className="text-slate-500 font-mono text-xs flex-shrink-0 mt-0.5">
                        {timestamp}
                      </span>
                      <p className="text-slate-700 flex-1">{segment.text}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Extracted Concepts Display */}
          {task?.extracted_concepts && task.extracted_concepts.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4 text-slate-900">
                💡 Concepts extraits ({task.extracted_concepts.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {task.extracted_concepts.map((concept, index) => (
                  <div
                    key={index}
                    className={`p-3 rounded-lg border-l-4 ${
                      concept.priority === 'high'
                        ? 'bg-green-50 border-green-500'
                        : concept.priority === 'medium'
                        ? 'bg-blue-50 border-blue-500'
                        : 'bg-slate-50 border-slate-400'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-semibold text-slate-900">{concept.name}</h4>
                        <p className="text-xs text-slate-500 mt-1">{concept.category}</p>
                        <p className="text-sm text-slate-600 mt-2">{concept.visual_description}</p>
                      </div>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        concept.priority === 'high'
                          ? 'bg-green-200 text-green-800'
                          : concept.priority === 'medium'
                          ? 'bg-blue-200 text-blue-800'
                          : 'bg-slate-200 text-slate-700'
                      }`}>
                        {concept.priority}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && !loading && (
        <div className="mt-6 space-y-6">
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700 font-semibold">❌ Erreur: {error}</p>
          </div>

          {/* Show transcript even on error */}
          {task?.transcript && task.transcript.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4 text-slate-900">
                📝 Transcription extraite ({task.transcript.length} segments)
              </h3>
              <div className="max-h-96 overflow-y-auto space-y-2 bg-slate-50 rounded-lg p-4">
                {task.transcript.map((segment, index) => {
                  const minutes = Math.floor(segment.start / 60);
                  const seconds = Math.floor(segment.start % 60);
                  const timestamp = `${minutes}:${seconds.toString().padStart(2, '0')}`;
                  return (
                    <div key={index} className="flex gap-3 text-sm border-b border-slate-200 pb-2">
                      <span className="text-slate-500 font-mono text-xs flex-shrink-0 mt-0.5">
                        {timestamp}
                      </span>
                      <p className="text-slate-700 flex-1">{segment.text}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Show extracted concepts even on error */}
          {task?.extracted_concepts && task.extracted_concepts.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4 text-slate-900">
                🎯 Concepts extraits ({task.extracted_concepts.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {task.extracted_concepts.map((concept, index) => {
                  const priorityColors = {
                    high: 'bg-red-100 text-red-800 border-red-300',
                    medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
                    low: 'bg-green-100 text-green-800 border-green-300'
                  };
                  return (
                    <div key={index} className="border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="font-semibold text-slate-900">{concept.name}</h4>
                        <span className={`px-2 py-1 text-xs rounded-full border ${priorityColors[concept.priority]}`}>
                          {concept.priority}
                        </span>
                      </div>
                      <p className="text-sm text-slate-600 mb-2">{concept.category}</p>
                      <p className="text-xs text-slate-500 italic">{concept.visual_description}</p>
                      {concept.context && (
                        <p className="text-xs text-slate-400 mt-2">Context: {concept.context}</p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Task Status */}
      {task && !loading && task.status === 'completed' && (
        <div className="mt-8 bg-white rounded-lg shadow-sm p-8 animate-fade-in">
          <h3 className="text-lg font-semibold mb-4 text-green-600">✅ Génération terminée!</h3>

          <div className="space-y-4">
            {task.generated_icons && task.generated_icons.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-lg font-medium text-green-800 mb-2">
                  {task.generated_icons.length} {task.generated_icons.length > 1 ? 'icônes générées' : 'icône générée'} avec succès!
                </p>
                <a
                  href="/icons"
                  className="inline-block mt-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Voir mes icônes →
                </a>
              </div>
            )}
            {task.message && (
              <p className="text-sm text-slate-600">{task.message}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
