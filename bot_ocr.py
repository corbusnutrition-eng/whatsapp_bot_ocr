from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import pytesseract
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    resp = MessagingResponse()

    # Extraer el mensaje de texto
    msg_body = request.form.get("Body", "")
    
    # Extraer si hay imagen
    num_media = int(request.form.get("NumMedia", 0))

    # Si NO hay imagen → responder normal
    if num_media == 0:
        resp.message(f"🟢 Bot OCR activo.\nRecibí tu mensaje:\n{msg_body}")
        return str(resp)

    # Si SÍ hay imagen → procesar OCR
    image_url = request.form.get("MediaUrl0")

    try:
        # Descargar imagen
        img_bytes = requests.get(image_url).content
        img = Image.open(BytesIO(img_bytes))

        # Aplicar OCR
        texto_extraido = pytesseract.image_to_string(img)

        resp.message(f"📄 *Texto detectado en la imagen:*\n\n{texto_extraido}")

    except Exception as e:
        resp.message(f"❌ Error procesando imagen: {str(e)}")

    return str(resp)


@app.route("/", methods=["GET"])
def home():
    return "Bot OCR funcionando", 200
