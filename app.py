from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route("/api/extract-color", methods=["POST"])
def extract_color():
    try:
        data = request.json

        # ตรวจสอบว่าเป็น Base64 ที่มี prefix data:image หรือไม่
        if "," in data["image"]:
            base64_str = data["image"].split(",")[1]
        else:
            base64_str = data["image"]

        # แปลงเป็น bytes และเปิดเป็นภาพ
        image_bytes = base64.b64decode(base64_str)
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # หาค่ากลางของภาพ
        width, height = img.size
        r, g, b = img.getpixel((width // 2, height // 2))

        return jsonify({"r": r, "g": g, "b": b})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# รัน Flask บน Render (ใช้ host 0.0.0.0 และ port 10000)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


