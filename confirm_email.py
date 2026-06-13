import os
from supabase import create_client, Client
from api_keys import keys

url: str = keys.SUPABASE_URL
key: str = keys.SUPABASE_SERVICE_KEY
supabase: Client = create_client(url, key)

try:
    print("Auto-confirming email for admin user...")
    # Get user by email to find the ID
    res = supabase.auth.admin.list_users()
    admin_id = None
    for u in res:
        if hasattr(u, 'email') and u.email == 'ramcraze3@gmail.com':
            admin_id = u.id
            break
        elif isinstance(u, dict) and u.get('email') == 'ramcraze3@gmail.com':
            admin_id = u.get('id')
            break
            
    if not admin_id:
        print("Could not find user in auth list, assuming ID: da7b46d9-97e2-451b-9037-76090bf39b6f")
        admin_id = "da7b46d9-97e2-451b-9037-76090bf39b6f"

    # Confirm email
    supabase.auth.admin.update_user_by_id(
        admin_id,
        {"email_confirm": True}
    )
    print("Email successfully confirmed! You can now log in.")
except Exception as e:
    print(f"Error occurred: {e}")
