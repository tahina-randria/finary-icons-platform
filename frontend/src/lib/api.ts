/**
 * API client for Finary Icons Platform
 */

import axios, { AxiosInstance } from 'axios';
import type {
  Icon,
  IconList,
  GenerateConceptRequest,
  GenerateYouTubeRequest,
  GenerateResponse,
  GenerationTask,
} from '@/types/icon';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        const message = error.response?.data?.detail || error.message || 'An error occurred';
        return Promise.reject(new Error(message));
      }
    );
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  // Health check
  async healthCheck() {
    return this.client.get('/health');
  }

  // Icons endpoints
  async listIcons(params?: {
    search?: string;
    category?: string;
    page?: number;
    page_size?: number;
  }): Promise<IconList> {
    return this.client.get('/api/icons', { params });
  }

  async getIcon(iconId: string): Promise<{ icon: Icon }> {
    return this.client.get(`/api/icons/${iconId}`);
  }

  async downloadIcon(iconId: string, size: string = 'original'): Promise<Blob> {
    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_API_URL}/api/icons/${iconId}/download`,
      {
        params: { size },
        responseType: 'blob',
      }
    );
    return response.data;
  }

  // Generation endpoints
  async generateFromConcept(request: GenerateConceptRequest): Promise<GenerateResponse> {
    return this.client.post('/api/generate/concept', request);
  }

  async generateFromYouTube(request: GenerateYouTubeRequest): Promise<GenerateResponse> {
    return this.client.post('/api/generate/youtube', request);
  }

  async getGenerationStatus(taskId: string): Promise<GenerationTask> {
    return this.client.get(`/api/generate/status/${taskId}`);
  }

  // Poll generation status until complete
  async pollGenerationStatus(
    taskId: string,
    onProgress?: (task: GenerationTask) => void,
    interval: number = 2000
  ): Promise<GenerationTask> {
    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const task = await this.getGenerationStatus(taskId);

          if (onProgress) {
            onProgress(task);
          }

          if (task.status === 'completed') {
            resolve(task);
          } else if (task.status === 'failed') {
            reject(new Error(task.error || 'Generation failed'));
          } else {
            setTimeout(poll, interval);
          }
        } catch (error) {
          reject(error);
        }
      };

      poll();
    });
  }
}

// Export singleton instance
export const api = new APIClient();
