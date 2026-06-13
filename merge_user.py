import os
from supabase import create_client, Client
from api_keys import keys

url = keys.SUPABASE_URL
key = keys.SUPABASE_SERVICE_KEY
supabase = create_client(url, key)

try:
    print("Deleting mismatched public user...")
    supabase.table('users').delete().eq('email', 'ramcraze3@gmail.com').execute()
    
    print("Re-inserting public user with correct Auth ID...")
    supabase.table("users").insert({
        "id": "781b201f-f1b0-4294-9b4c-26ba94e5675b",
        "email": "ramcraze3@gmail.com",
        "full_name": "Ram A",
        "role": "Team Member"
    }).execute()
    print("Done!")
except Exception as e:
    print(f"Error: {e}")
