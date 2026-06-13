import os
from supabase import create_client, Client
from api_keys import keys

url: str = keys.SUPABASE_URL
key: str = keys.SUPABASE_SERVICE_KEY
supabase: Client = create_client(url, key)

try:
    print("Fetching all Auth users...")
    all_users = supabase.auth.admin.list_users()
    users_list = all_users if isinstance(all_users, list) else getattr(all_users, 'users', [])
    
    print(f"Found {len(users_list)} Auth users. Deleting...")
    for user in users_list:
        try:
            supabase.auth.admin.delete_user(user.id)
            print(f"Deleted Auth user: {user.email}")
        except Exception as e:
            print(f"Failed to delete Auth user {user.email}: {e}")

    print("Deleting all from public.users...")
    res = supabase.table('users').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    print("Public users deleted!")
    
except Exception as e:
    print(f"Error: {e}")
