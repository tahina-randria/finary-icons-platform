/**
 * TypeScript type definitions for icons and generation
 */

export enum IconCategory {
  FINANCE_INVESTISSEMENT = "finance_investissement",
  IMMOBILIER = "immobilier",
  VEHICULES = "vehicules",
  METIERS = "metiers",
  OBJETS = "objets",
  LIEUX = "lieux",
  DEVISES = "devises",
  ACTIONS = "actions",
  ETATS = "etats",
  ORGANISMES = "organismes",
  NOURRITURE = "nourriture",
  SPORT = "sport",
  OTHER = "other",
}

export interface Icon {
  id: string;
  name: string;
  category: IconCategory;
  prompt: string;
  animation_prompt?: string;
  image_url: string;
  thumbnail_url?: string;
  tags: string[];
  download_count: number;
  created_at: string;
  updated_at?: string;
}

export interface IconList {
  icons: Icon[];
  total: number;
  page: number;
  page_size: number;
  success: boolean;
}

export enum GenerationStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  EXTRACTING_CONCEPTS = "extracting_concepts",
  GENERATING_IMAGES = "generating_images",
  REMOVING_BACKGROUNDS = "removing_backgrounds",
  UPLOADING = "uploading",
  COMPLETED = "completed",
  FAILED = "failed",
}

export enum ConceptPriority {
  HIGH = "high",
  MEDIUM = "medium",
  LOW = "low",
}

export interface ConceptExtraction {
  name: string;
  category: string;
  priority: ConceptPriority;
  visual_description: string;
  context?: string;
}

export interface TranscriptSegment {
  text: string;
  start: number;
  duration: number;
}

export interface GenerationTask {
  task_id: string;
  status: GenerationStatus;
  progress: number;
  message?: string;
  created_at: string;
  updated_at: string;
  completed_at?: string;
  error?: string;
  extracted_concepts?: ConceptExtraction[];
  generated_icons?: string[];
  transcript?: TranscriptSegment[];
  transcript_text?: string;
  metadata?: Record<string, any>;
}

export interface GenerateConceptRequest {
  concept: string;
  category?: string;
  style?: string;
  size?: string;
  include_animation_prompt?: boolean;
}

export interface GenerateYouTubeRequest {
  youtube_url: string;
  max_concepts?: number;
  min_priority?: ConceptPriority;
  style?: string;
  auto_generate?: boolean;
}

export interface GenerateResponse {
  task_id: string;
  status: GenerationStatus;
  message: string;
  estimated_time_seconds?: number;
}

export const CATEGORY_LABELS: Record<IconCategory, string> = {
  [IconCategory.FINANCE_INVESTISSEMENT]: "Finance & Investissement",
  [IconCategory.IMMOBILIER]: "Immobilier",
  [IconCategory.VEHICULES]: "Véhicules",
  [IconCategory.METIERS]: "Métiers",
  [IconCategory.OBJETS]: "Objets",
  [IconCategory.LIEUX]: "Lieux",
  [IconCategory.DEVISES]: "Devises",
  [IconCategory.ACTIONS]: "Actions",
  [IconCategory.ETATS]: "États",
  [IconCategory.ORGANISMES]: "Organismes",
  [IconCategory.NOURRITURE]: "Nourriture",
  [IconCategory.SPORT]: "Sport",
  [IconCategory.OTHER]: "Autre",
};
