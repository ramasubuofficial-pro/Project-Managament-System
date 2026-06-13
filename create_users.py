import os
from supabase import create_client, Client
from api_keys import keys

url = keys.SUPABASE_URL
key = keys.SUPABASE_SERVICE_KEY
supabase = create_client(url, key)

users_to_create = [
    {"email": "ramcraze3@gmail.com", "password": "password123", "name": "Ram A"},
    {"email": "ramasubuofficial@gmail.com", "password": "password123", "name": "Ramasubramaniyan"},
    {"email": "hogwartzdigitalworks@gmail.com", "password": "password123", "name": "Hogwartz Admin"}
]

for u in users_to_create:
    try:
        res = supabase.auth.admin.create_user({
            "email": u["email"],
            "password": u["password"],
            "email_confirm": True,
            "user_metadata": {"full_name": u["name"]}
        })
        user_id = res.user.id
        print(f"Created Auth User: {u['email']} (ID: {user_id})")
        
        # Insert into DB
        supabase.table("users").insert({
            "id": user_id,
            "email": u["email"],
            "full_name": u["name"],
            "role": "Admin" if "Admin" in u["name"] else "Team Member"
        }).execute()
        print(f"Inserted into public.users: {u['email']}")
    except Exception as e:
        print(f"Error creating {u['email']}: {e}")
