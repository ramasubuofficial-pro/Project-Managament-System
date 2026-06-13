import os
from supabase import create_client, Client
from api_keys import keys

url = keys.SUPABASE_URL
key = keys.SUPABASE_SERVICE_KEY
supabase = create_client(url, key)

# Delete ghost user from public.users
try:
    print("Deleting ghost user...")
    supabase.table('users').delete().eq('email', 'ramcraze3@gmail.com').execute()
    print("Ghost user deleted!")
    
    # Re-insert with the correct Auth ID
    # Get the auth user
    users = supabase.auth.admin.list_users()
    users_list = users if isinstance(users, list) else getattr(users, 'users', [])
    
    target_user = next((u for u in users_list if u.email == 'ramcraze3@gmail.com'), None)
    
    if target_user:
        supabase.table("users").insert({
            "id": target_user.id,
            "email": "ramcraze3@gmail.com",
            "full_name": "Ram A",
            "role": "Team Member"
        }).execute()
        print("Successfully re-inserted ramcraze3@gmail.com!")
except Exception as e:
    print(f"Error: {e}")
