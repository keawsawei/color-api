from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "Color Extractor API is running!"

@app.route('/getrgb', methods=['POST'])
def get_rgb():
    try:
        data = request.get_json()
        img_data = data['image']
        img_bytes = base64.b64decode(img_data.split(",")[-1])
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        center = image.getpixel((image.width // 2, image.height // 2))
        return jsonify({"r": center[0], "g": center[1], "b": center[2]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
