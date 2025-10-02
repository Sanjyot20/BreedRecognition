from supabase import create_client, Client
import os

SUPABASE_URL = "https://rnxeqmyfbyyzezesngdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJueGVxbXlmYnl5emV6ZXNuZ2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzE2ODksImV4cCI6MjA3NDMwNzY4OX0._Bm1lEEszsjTSUbXDIg_JzHvuhOraA3L8KgGGkA6fdE"
BUCKET_NAME = "models"
MODEL_FILE = "breed_model.h5"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Check model in bucket
files = supabase.storage.from_(BUCKET_NAME).list()
if any(f['name'] == MODEL_FILE for f in files):
    print(f"✅ {MODEL_FILE} exists in bucket '{BUCKET_NAME}'")
else:
    print(f"❌ {MODEL_FILE} not found in bucket '{BUCKET_NAME}'")

# Download model locally
os.makedirs("model", exist_ok=True)
response = supabase.storage.from_(BUCKET_NAME).download(MODEL_FILE)
if response:
    with open(os.path.join("model", MODEL_FILE), "wb") as f:
        f.write(response)
    print(f"✅ Model downloaded to 'model/{MODEL_FILE}'")
else:
    print("❌ Could not download model")

# List last 5 predictions
response = supabase.table("predictions").select("*").order("created_at", desc=True).limit(5).execute()
if response.data:
    print("\nLast 5 predictions:")
    for row in response.data:
        print(row)
else:
    print("No predictions found")
