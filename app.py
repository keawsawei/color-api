from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Color Extractor API is running!"

@app.route('/getrgb', methods=['POST'])
def get_rgb():
    try:
        data = request.get_json()
        img_data = data['image']
        
        # แยก header (data:image/jpeg;base64,) ออก
        base64_str = img_data.split(",")[-1]
        img_bytes = base64.b64decode(base64_str)
        
        image = Image.open(io.BytesIO(img_bytes))
        image = image.convert("RGB")
        
        # เอาค่า pixel ตรงกลางภาพ
        w, h = image.size
        r, g, b = image.getpixel((w // 2, h // 2))
        
        return jsonify({"r": r, "g": g, "b": b})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
