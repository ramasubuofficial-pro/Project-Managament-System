import os
from supabase import create_client, Client
from api_keys import keys

url = keys.SUPABASE_URL
key = keys.SUPABASE_SERVICE_KEY
supabase = create_client(url, key)

try:
    print("--- AUTH USERS ---")
    auth_users = supabase.auth.admin.list_users()
    users_list = auth_users if isinstance(auth_users, list) else getattr(auth_users, 'users', [])
    for u in users_list:
        if u.email == 'ramcraze3@gmail.com':
            print(f"Auth ID: {u.id}")

    print("--- PUBLIC USERS ---")
    res = supabase.table('users').select('*').eq('email', 'ramcraze3@gmail.com').execute()
    for row in res.data:
        print(f"Public ID: {row['id']}")
except Exception as e:
    print(f"Error: {e}")
