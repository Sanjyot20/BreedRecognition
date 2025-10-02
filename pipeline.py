import os
import uuid
from supabase import create_client
from predict import predict_breed

# ===== CONFIG =====
SUPABASE_URL = "https://rnxeqmyfbyyzezesngdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJueGVxbXlmYnl5emV6ZXNuZ2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzE2ODksImV4cCI6MjA3NDMwNzY4OX0._Bm1lEEszsjTSUbXDIg_JzHvuhOraA3L8KgGGkA6fdE"
IMAGE_BUCKET = "images"
IMAGE_PATH = "images/test.jpg"
# ==================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Upload image to Supabase
image_name = os.path.basename(IMAGE_PATH)
image_storage_path = f"{uuid.uuid4()}_{image_name}"
with open(IMAGE_PATH, "rb") as f:
    supabase.storage.from_(IMAGE_BUCKET).upload(image_storage_path, f, {"upsert": True})

image_url = supabase.storage.from_(IMAGE_BUCKET).get_public_url(image_storage_path).public_url
print(f"✅ Image uploaded: {image_url}")

# Predict breed
breed_id, breed_name, confidence = predict_breed(IMAGE_PATH)
print(f"Predicted: {breed_name} (ID: {breed_id}) with confidence {confidence:.2f}")

# Insert prediction record
user_id = str(uuid.uuid4())
prediction_id = str(uuid.uuid4())

data = {
    "id": prediction_id,
    "user_id": user_id,
    "image_url": image_url,
    "predicted_breed": breed_id,
    "confidence": confidence
}

response = supabase.table("predictions").insert(data).execute()
print("✅ Prediction saved to Supabase!")
