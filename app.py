from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import io
import base64

app = FastAPI()

class ImageInput(BaseModel):
    image: str  # base64 string

@app.post("/api/extract-color")
def extract_color(data: ImageInput):
    try:
        # ตัด prefix "data:image/png;base64," ออก ถ้ามี
        if "," in data.image:
            base64_data = data.image.split(",")[1]
        else:
            base64_data = data.image

        # แปลง base64 เป็น bytes
        image_bytes = base64.b64decode(base64_data)

        # เปิดเป็นภาพ
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # ดึง pixel ตำแหน่งกลางภาพ
        width, height = img.size
        r, g, b = img.getpixel((width // 2, height // 2))

        return {"r": r, "g": g, "b": b}

    except Exception as e:
        return {"error": str(e)}
