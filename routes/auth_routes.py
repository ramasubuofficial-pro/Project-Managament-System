from flask import Blueprint, redirect, url_for, session, request, render_template, jsonify
from utils import supabase, get_supabase_admin
import requests
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    # If already logged in, redirect to dashboard
    if 'user' in session:
        return redirect(url_for('views.dashboard'))
    return render_template('login.html')

@auth_bp.route('/register')
def register():
    if 'user' in session:
        return redirect(url_for('views.dashboard'))
    return render_template('register.html')

@auth_bp.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@auth_bp.route('/reset-password')
def reset_password():
    return render_template('reset_password.html')

@auth_bp.route('/google')
def google_auth():
    # Redirect to Supabase Google Auth (simplified for this demo, usually handled via frontend or direct link)
    # Since we are using Supabase, it provides a built-in auth URL.
    # However, for a strict Flask + Supabase OAuth flow, we might handle the callback.
    # For simplicity, we'll assume the client-side Supabase Auth or a direct redirect.
    
    # Actually, the user prompt says "Google OAuth 2.0 for authentication... On first login: Create user record".
    # Supabase handles this automatically if we use their Auth. 
    # Let's rely on client-side Supabase Auth for the initial login to get the JWT, 
    # then send that to the server to set the session, OR use server-side OAuth flow.
    # Given the strict requirement for "Flask backend", we'll implement a route that initiates the flow
    # but Supabase Python client is mostly for data. Supabase GoTrue (Auth) is often easier on client-side.
    # But let's try server-side redirect if possible or just render the login page with the button.
    
    return render_template('login.html') # The login page will handle the actual button click/redirect.

@auth_bp.route('/callback')
def auth_callback():
    # In a real app, Supabase redirects here with an access token in the hash (client-side) 
    # or code (server-side) depending on flow.
    # Since Supabase default is implicit/PKCE for client, we often process it on client and then POST to server to set a session cookie.
    return render_template('auth_callback.html')

@auth_bp.route('/api/set-session', methods=['POST'])
def set_session():
    data = request.json
    access_token = data.get('access_token')
    user_data = data.get('user')
    
    if access_token and user_data:
        user_id = user_data.get('id')
        email = user_data.get('email')
        full_name = user_data.get('user_metadata', {}).get('full_name', '')
        avatar_url = user_data.get('user_metadata', {}).get('avatar_url', '')

        try:
            # STRICT AUTH CHECK:
            # User must ALREADY exist in public.users (via Invite) to log in.
            
            # Use Admin Client to bypass RLS for this check
            # (Because 'supabase' client is Anon and might not be able to read users table if RLS is strict)
            admin_client = get_supabase_admin()
            verifier = admin_client if admin_client else supabase
            
            # Fetch existing user including workspace_id
            existing = verifier.table('users').select('role, full_name, workspace_id').eq('id', user_id).execute()
            
            if not existing.data:
                # Check for ID mismatch (e.g., Supabase created a new Auth ID for Google OAuth)
                email_check = verifier.table('users').select('id, role, workspace_id').eq('email', email).execute()
                if email_check.data:
                    old_id = email_check.data[0]['id']
                    db_role = email_check.data[0].get('role', 'Team Member')
                    db_workspace_id = email_check.data[0].get('workspace_id')
                    print(f"ID mismatch for {email}. Updating public.users from {old_id} to {user_id}")
                    # Update the ID to match the new Auth ID instead of crashing
                    verifier.table('users').update({'id': user_id}).eq('email', email).execute()
                    db_name = full_name or email.split('@')[0]
                else:
                    # User completely not found in DB -> Auto register as Admin
                    print(f"New User Signup: {email} ({user_id})")
                    db_name = full_name or email.split('@')[0]
                    
                    # 1. Create a new Workspace for this user
                    workspace_name = f"{db_name}'s Workspace"
                    workspace_res = verifier.table('workspaces').insert({'name': workspace_name}).execute()
                    db_workspace_id = workspace_res.data[0]['id']
                    
                    # 2. Insert User
                    insert_payload = {
                        'id': user_id,
                        'email': email,
                        'full_name': db_name,
                        'role': 'Admin',
                        'avatar_url': avatar_url,
                        'workspace_id': db_workspace_id
                    }
                    verifier.table('users').insert(insert_payload).execute()
                    db_role = 'Admin'
            else:
                # --- User is Valid ---
                record = existing.data[0]
                db_role = record.get('role', 'Team Member')
                db_name = record.get('full_name', email.split('@')[0])
                db_workspace_id = record.get('workspace_id')

                # Update details (Avatar/Name) but keep Role
                update_payload = {
                    'email': email,
                    'avatar_url': avatar_url
                }
                if not db_name and full_name:
                    update_payload['full_name'] = full_name
                elif db_name:
                    user_data['user_metadata']['full_name'] = db_name # Session uses DB name
                    user_data['full_name'] = db_name

                supabase.table('users').update(update_payload).eq('id', user_id).execute()

            # Set Session
            user_data['user_metadata']['full_name'] = db_name
            user_data['user_metadata']['workspace_id'] = db_workspace_id
            user_data['role'] = db_role
            
            session['user'] = user_data
            session.modified = True
            
            return jsonify({"status": "success"}), 200

        except Exception as e:
            print(f"Error syncing user: {e}")
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid payload"}), 400

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login', force_logout=1))
