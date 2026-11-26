import cv2
import numpy as np

from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_qr():
    data = request.form.get("data")

    if not data:
        return "Please enter text or URL"

    qr = qrcode.make(data)

    img_io = BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)

    return send_file(
        img_io,
        mimetype="image/png",
        as_attachment=True,
        download_name="my_qr_code.png"
    )
@app.route("/scan", methods=["POST"])
def scan_qr():
    file = request.files.get("qr_image")

    if not file:
        return "Please upload a QR code image"

    image_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)

    if data:
        return render_template("scan.html", scanned_data=data)
    else:
        return render_template("scan.html", scanned_data="No QR code found!")

@app.route("/generate")
def generate_page():
    return render_template("generate.html")


@app.route("/scan")
def scan_page():
    return render_template("scan.html")


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
