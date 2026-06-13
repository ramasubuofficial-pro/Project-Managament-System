import os
from supabase import create_client, Client
from api_keys import keys

url: str = keys.SUPABASE_URL
key: str = keys.SUPABASE_SERVICE_KEY
supabase: Client = create_client(url, key)

try:
    print("Fetching projects with admin_client...")
    res = supabase.table('projects').select('*').execute()
    print(f"Projects count: {len(res.data)}")
    for p in res.data:
        print(f"Project: {p['title']}, workspace: {p.get('workspace_id')}")
        
except Exception as e:
    print(f"Error: {e}")
