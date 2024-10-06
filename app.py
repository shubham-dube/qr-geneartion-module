import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from pydantic import BaseModel

class QrData(BaseModel):
    id: str
    sessionId: str
    courseId: int
    className: str
    duration: str
    startTime: str
    timestamp: str


app = FastAPI()

def generateQR(data: QrData):
    QR = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=7,
        border=4,
    )

    QR.add_data(data)
    QR.make(fit=True)

    qrImage = QR.make_image(
        image_factory=StyledPilImage, 
        module_drawer=RoundedModuleDrawer(), 
        color_mask=RadialGradiantColorMask()
    )

    byteArray = BytesIO()
    qrImage.save(byteArray, format='PNG')
    byteArray.seek(0)
    
    return byteArray

@app.post("/generateQrCode")
def generateQrCode(qrData: QrData):
    img_stream = generateQR(qrData)
    return StreamingResponse(img_stream, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)