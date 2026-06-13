import os
from supabase import create_client
from api_keys import keys
import requests

# We cannot execute DDL (CREATE TABLE) easily via standard Supabase Python client.
# We must use the Supabase REST API via `postgres-meta` or execute a custom RPC function.
# But actually, the easiest way to run SQL programmatically on Supabase is if we create an RPC function.
# Since we don't have direct SQL access, we can instruct the user to run the SQL via their dashboard, OR 
# we can use psycopg2 if we have the Postgres connection string.
# Let's check api_keys.py for a DB URL.

def main():
    print("Please run the following SQL script in your Supabase SQL Editor:")
    sql = """
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
    """
    with open('workspace_migration.sql', 'w') as f:
        f.write(sql)
    print("Created workspace_migration.sql")

if __name__ == '__main__':
    main()
