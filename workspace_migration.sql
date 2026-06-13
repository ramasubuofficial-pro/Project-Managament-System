
-- 1. Create Workspaces Table
CREATE TABLE IF NOT EXISTS workspaces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Add Workspace ID to Users
ALTER TABLE users ADD COLUMN IF NOT EXISTS workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE;

-- 3. Add Workspace ID to Projects
ALTER TABLE projects ADD COLUMN IF NOT EXISTS workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE;

-- 4. Create a Default Legacy Workspace for existing users
DO $$
DECLARE
    legacy_workspace_id UUID;
BEGIN
    IF EXISTS (SELECT 1 FROM users WHERE workspace_id IS NULL) THEN
        INSERT INTO workspaces (name) VALUES ('Legacy Workspace') RETURNING id INTO legacy_workspace_id;
        
        UPDATE users SET workspace_id = legacy_workspace_id WHERE workspace_id IS NULL;
        UPDATE projects SET workspace_id = legacy_workspace_id WHERE workspace_id IS NULL;
    END IF;
END $$;
    