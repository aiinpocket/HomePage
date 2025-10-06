-- 允許 projects 表的 user_id 為 NULL（匿名用戶）
-- Migration: 003_allow_anonymous_projects.sql
-- Date: 2025-10-06

-- 修改外鍵約束，允許 NULL
ALTER TABLE projects
DROP CONSTRAINT IF EXISTS projects_user_id_fkey;

ALTER TABLE projects
ALTER COLUMN user_id DROP NOT NULL;

-- 重新添加外鍵約束（允許 NULL）
ALTER TABLE projects
ADD CONSTRAINT projects_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;

-- 為匿名用戶的專案添加索引
CREATE INDEX IF NOT EXISTS idx_projects_anonymous
ON projects(id)
WHERE user_id IS NULL;
