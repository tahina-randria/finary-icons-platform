-- Finary Icons Platform - Storage Setup
-- Migration: 002_storage_setup.sql

-- Create storage bucket for icons
INSERT INTO storage.buckets (id, name, public)
VALUES ('icons', 'icons', true)
ON CONFLICT (id) DO NOTHING;

-- Storage policies for icons bucket

-- Allow public read access to all icons
CREATE POLICY "Public read access for icons"
ON storage.objects FOR SELECT
USING (bucket_id = 'icons');

-- Allow authenticated users to upload icons
CREATE POLICY "Authenticated users can upload icons"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'icons');

-- Allow authenticated users to update their own uploads
CREATE POLICY "Authenticated users can update icons"
ON storage.objects FOR UPDATE
TO authenticated
USING (bucket_id = 'icons');

-- Allow authenticated users to delete icons
CREATE POLICY "Authenticated users can delete icons"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'icons');

-- Service role has full access (for backend operations)
CREATE POLICY "Service role has full access"
ON storage.objects FOR ALL
TO service_role
USING (bucket_id = 'icons');

-- Create folder structure (optional)
-- Icons will be organized as:
-- /icons/original/{icon_id}.png
-- /icons/2k/{icon_id}.png
-- /icons/1k/{icon_id}.png
-- /icons/thumbnails/{icon_id}.png

COMMENT ON POLICY "Public read access for icons" ON storage.objects
IS 'Anyone can view and download icon images';

COMMENT ON POLICY "Authenticated users can upload icons" ON storage.objects
IS 'Authenticated users can upload new icon images';
