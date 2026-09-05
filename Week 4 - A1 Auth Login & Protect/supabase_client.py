import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment configuration from .env in current directory
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your_anon_key")

# Initialize and export shared Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
