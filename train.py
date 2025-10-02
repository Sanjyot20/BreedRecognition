import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator # pyright: ignore[reportMissingImports]
from supabase import create_client

# ===== CONFIG =====
SUPABASE_URL = "https://rnxeqmyfbyyzezesngdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJueGVxbXlmYnl5emV6ZXNuZ2RvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODczMTY4OSwiZXhwIjoyMDc0MzA3Njg5fQ.ncUmA1HnkJwl-2FV8km5vjBRSlYxo9nHCqEEmxF-O1w"
BUCKET_NAME = "models"
MODEL_DIR = "model"
MODEL_FILE = "breed_model.h5"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
DATASET_DIR = "dataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10
# ==================

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
os.makedirs(MODEL_DIR, exist_ok=True)

train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_gen = train_datagen.flow_from_directory(DATASET_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, subset="training")
val_gen = train_datagen.flow_from_directory(DATASET_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, subset="validation")

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(train_gen.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("🚀 Training model...")
history = model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

model.save(MODEL_PATH)
print(f"✅ Model saved at {MODEL_PATH}")

# Upload to Supabase
with open(MODEL_PATH, "rb") as f:
    supabase.storage.from_(BUCKET_NAME).upload(MODEL_FILE, f, {"upsert": True})
print(f"✅ Model uploaded to Supabase bucket '{BUCKET_NAME}/{MODEL_FILE}'")
