-- Finary Icons Platform - Initial Database Schema
-- Migration: 001_initial_schema.sql

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Icons table
CREATE TABLE IF NOT EXISTS icons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    prompt TEXT NOT NULL,
    animation_prompt TEXT,
    image_url TEXT NOT NULL,
    thumbnail_url TEXT,
    tags TEXT[] DEFAULT '{}',
    download_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Generations table (for tracking generation tasks)
CREATE TABLE IF NOT EXISTS generations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    message TEXT,
    source_type VARCHAR(50) NOT NULL, -- 'concept' or 'youtube'
    source_data JSONB NOT NULL,
    extracted_concepts JSONB,
    generated_icons TEXT[] DEFAULT '{}', -- Array of icon IDs
    error TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Concepts table (for tracking extracted concepts)
CREATE TABLE IF NOT EXISTS concepts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL, -- 'high', 'medium', 'low'
    visual_description TEXT NOT NULL,
    context TEXT,
    icon_id UUID REFERENCES icons(id) ON DELETE SET NULL,
    source_generation_id UUID REFERENCES generations(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_icons_category ON icons(category);
CREATE INDEX idx_icons_name ON icons USING gin(to_tsvector('english', name));
CREATE INDEX idx_icons_tags ON icons USING gin(tags);
CREATE INDEX idx_icons_created_at ON icons(created_at DESC);

CREATE INDEX idx_generations_task_id ON generations(task_id);
CREATE INDEX idx_generations_status ON generations(status);
CREATE INDEX idx_generations_created_at ON generations(created_at DESC);

CREATE INDEX idx_concepts_name ON concepts(name);
CREATE INDEX idx_concepts_category ON concepts(category);
CREATE INDEX idx_concepts_icon_id ON concepts(icon_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_icons_updated_at
    BEFORE UPDATE ON icons
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_generations_updated_at
    BEFORE UPDATE ON generations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to increment download count
CREATE OR REPLACE FUNCTION increment_download_count(icon_uuid UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE icons
    SET download_count = download_count + 1
    WHERE id = icon_uuid;
END;
$$ LANGUAGE plpgsql;

-- Comments
COMMENT ON TABLE icons IS 'Generated icons with metadata and storage URLs';
COMMENT ON TABLE generations IS 'Icon generation tasks and their status';
COMMENT ON TABLE concepts IS 'Extracted concepts from YouTube transcripts';

COMMENT ON COLUMN icons.tags IS 'Searchable tags for filtering icons';
COMMENT ON COLUMN icons.metadata IS 'Additional metadata (generation parameters, etc.)';
COMMENT ON COLUMN generations.source_type IS 'Type of generation source: concept or youtube';
COMMENT ON COLUMN generations.source_data IS 'Original request data (concept text or YouTube URL)';
COMMENT ON COLUMN concepts.priority IS 'Concept importance: high, medium, or low';
