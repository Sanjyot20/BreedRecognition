from pipeline import upload_and_save_prediction

import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from predict import predict_breed
from supabase import create_client

# ===== CONFIG =====
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
SUPABASE_URL = "https://rnxeqmyfbyyzezesngdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJueGVxbXlmYnl5emV6ZXNuZ2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzE2ODksImV4cCI6MjA3NDMwNzY4OX0._Bm1lEEszsjTSUbXDIg_JzHvuhOraA3L8KgGGkA6fdE"
IMAGE_BUCKET = "images"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===== Helpers =====
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ===== Routes =====
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Predict breed
            breed_id, breed_name, confidence = predict_breed(file_path)

            # Upload to Supabase
            with open(file_path, "rb") as f:
                storage_path = f"{filename}"
                supabase.storage.from_(IMAGE_BUCKET).upload(storage_path, f, {"upsert": True})
                image_url = supabase.storage.from_(IMAGE_BUCKET).get_public_url(storage_path).public_url

            return render_template("result.html", breed=breed_name, confidence=confidence, image_url=image_url)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
