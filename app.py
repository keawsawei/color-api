from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)  # ✅ ต้องใช้ __name__

@app.route('/')
def home():
    return 'Color Extractor API is running!'  # ✅ ต้องมี indent

@app.route('/getrgb', methods=['POST'])
def get_rgb():
    try:
        data = request.get_json()
        img_data = data['image']

        # แปลง base64 เป็นภาพ
        img_bytes = base64.b64decode(img_data.split(",")[-1])
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img = img.resize((1, 1))  # ย่อให้เหลือ 1 พิกเซลเฉลี่ย
        r, g, b = img.getpixel((0, 0))
        return jsonify({
            "r": r,
            "g": g,
            "b": b
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':  # ✅ ต้องใช้ __name__ == '__main__'
    app.run(host='0.0.0.0', port=3000)
