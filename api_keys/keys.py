import os
from dotenv import load_dotenv

load_dotenv()

def clean_env(key, default=""):
    val = os.getenv(key, default)
    if val:
        val = val.strip().strip('"').strip("'")
    return val

# Supabase Configuration
SUPABASE_URL = clean_env("SUPABASE_URL")
SUPABASE_KEY = clean_env("SUPABASE_ANON_KEY", clean_env("SUPABASE_KEY"))
SUPABASE_SERVICE_KEY = clean_env("SUPABASE_SERVICE_KEY")

# Google OAuth Configuration
GOOGLE_CLIENT_ID = clean_env("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = clean_env("GOOGLE_CLIENT_SECRET")

# Flask Configuration
SECRET_KEY = clean_env("SECRET_KEY", "fallback-secret-key-change-me")

# Gemini AI Configuration
GEMINI_API_KEY = clean_env("GEMINI_API_KEY")

# SMTP Email Configuration
SMTP_EMAIL = clean_env("SMTP_EMAIL")
SMTP_PASSWORD = clean_env("SMTP_PASSWORD")
