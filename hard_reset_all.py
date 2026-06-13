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

    print("Wiping all public data...")
    # Because of foreign key constraints, order matters or cascade will handle it.
    # But explicitly deleting them is safest.
    
    # Workspaces cascades to users and projects.
    supabase.table('workspaces').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    print("Workspaces deleted!")
    
    supabase.table('users').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    print("Users deleted!")
    
    supabase.table('projects').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    print("Projects deleted!")

    supabase.table('tasks').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    print("Tasks deleted!")
    
    supabase.table('notifications').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    print("Notifications deleted!")
    
    supabase.table('attendance').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    print("Attendance deleted!")
    
    print("Hard reset complete!")

except Exception as e:
    print(f"Error: {e}")
