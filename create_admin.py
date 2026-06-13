import os
from supabase import create_client, Client
from api_keys import keys

url: str = keys.SUPABASE_URL
key: str = keys.SUPABASE_SERVICE_KEY
supabase: Client = create_client(url, key)

try:
    # Sign up the user in Supabase Auth
    print(f"Signing up user: ramcraze3@gmail.com...")
    res = supabase.auth.sign_up({
      "email": "ramcraze3@gmail.com",
      "password": "ramcraze3"
    })
    
    if res.user:
        print(f"User created in Auth with ID: {res.user.id}")
        
        # Insert or update the user in the 'users' table as Admin
        # First check if exists
        existing = supabase.table("users").select("*").eq("email", "ramcraze3@gmail.com").execute()
        
        if existing.data:
            print("User already exists in 'users' table, updating role to Admin...")
            supabase.table("users").update({"role": "Admin"}).eq("email", "ramcraze3@gmail.com").execute()
        else:
            print("Inserting new Admin user into 'users' table...")
            supabase.table("users").insert({
                "id": res.user.id,
                "email": "ramcraze3@gmail.com",
                "full_name": "Accio Hub Admin",
                "role": "Admin"
            }).execute()
            
        print("Admin user setup successfully!")
    else:
        print("Sign up failed, no user returned.")
except Exception as e:
    print(f"Error occurred: {e}")
