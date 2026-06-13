import os
from supabase import create_client, Client
from api_keys import keys

url = keys.SUPABASE_URL
key = keys.SUPABASE_SERVICE_KEY
supabase = create_client(url, key)

try:
    print("Deleting all Auth users matching ramcraze3@gmail.com...")
    auth_users = supabase.auth.admin.list_users()
    users_list = auth_users if isinstance(auth_users, list) else getattr(auth_users, 'users', [])
    for u in users_list:
        if u.email == 'ramcraze3@gmail.com':
            supabase.auth.admin.delete_user(u.id)
            print(f"Deleted Auth ID: {u.id}")

    print("Deleting from public.users...")
    supabase.table('users').delete().eq('email', 'ramcraze3@gmail.com').execute()
    
    print("Re-creating single user...")
    res = supabase.auth.admin.create_user({
        "email": "ramcraze3@gmail.com",
        "password": "password123",
        "email_confirm": True,
        "user_metadata": {"full_name": "Ram A"}
    })
    
    user_id = res.user.id
    print(f"New Auth ID: {user_id}")
    
    supabase.table("users").insert({
        "id": user_id,
        "email": "ramcraze3@gmail.com",
        "full_name": "Ram A",
        "role": "Team Member"
    }).execute()
    print("Successfully inserted into public.users with exact same ID!")
except Exception as e:
    print(f"Error: {e}")
