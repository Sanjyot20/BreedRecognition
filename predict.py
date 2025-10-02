import tensorflow as tf
import numpy as np
from PIL import Image

# Map class names to breed IDs
class_names = ['Gir', 'Sahiwal', 'Red Sindhi', 'Murrah', 'Jaffarabadi', 'Bhadawari']
breed_name_to_id = {'Gir': 1, 'Sahiwal': 2, 'Red Sindhi': 3, 'Murrah': 4, 'Jaffarabadi': 5, 'Bhadawari': 6}

MODEL_PATH = "model/breed_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(path, img_size=(224, 224)):
    img = Image.open(path).convert('RGB')
    img = img.resize(img_size)
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)

def predict_breed(image_path):
    x = preprocess_image(image_path)
    probs = model.predict(x)[0]
    idx = int(np.argmax(probs))
    breed_name = class_names[idx]
    confidence = float(probs[idx])
    return breed_name_to_id[breed_name], breed_name, confidence
