from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running!"

@app.route("/api/extract-color", methods=["POST"])
def extract_color():
    try:
        data = request.get_json()
        image_data = data["image"]

        # ตัด prefix ถ้ามี (data:image/png;base64,...)
        if "," in image_data:
            image_data = image_data.split(",")[1]

        # แปลง base64 เป็นภาพ
        img_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # หาค่าเฉลี่ย RGB
        pixels = list(image.getdata())
        r = int(sum(p[0] for p in pixels) / len(pixels))
        g = int(sum(p[1] for p in pixels) / len(pixels))
        b = int(sum(p[2] for p in pixels) / len(pixels))

        return jsonify({"r": r, "g": g, "b": b})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

