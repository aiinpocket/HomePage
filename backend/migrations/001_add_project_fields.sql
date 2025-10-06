-- Migration: Add new fields to Project table for async generation
-- Date: 2025-10-06

-- Add images_data column to store base64 encoded images
ALTER TABLE projects ADD COLUMN IF NOT EXISTS images_data TEXT;

-- Add html_content column to store generated HTML
ALTER TABLE projects ADD COLUMN IF NOT EXISTS html_content TEXT;

-- Add error_message column for failed generations
ALTER TABLE projects ADD COLUMN IF NOT EXISTS error_message TEXT;

-- Update status values if needed (existing values: draft, generating, completed, failed)
-- No changes needed for status column

-- Add index on status for filtering
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);

-- Add index on user_id and status for user project queries
CREATE INDEX IF NOT EXISTS idx_projects_user_status ON projects(user_id, status);

COMMENT ON COLUMN projects.images_data IS 'JSON format: {"logo": "base64...", "portfolio1": "base64..."}';
COMMENT ON COLUMN projects.html_content IS 'Generated HTML content with image placeholders';
COMMENT ON COLUMN projects.error_message IS 'Error message if generation failed';
