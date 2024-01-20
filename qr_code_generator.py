from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import os

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code():
    name = request.form.get('name', '')
    phone = request.form.get('phone', '')

    if not name or not phone:
        return "Name and phone are required."

    data = f"Name: {name}\nPhone: {phone}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join(app.root_path, "static","qrcodes", f"{name}qrcode.png")
    img.save(img_path)

    return send_file(img_path, as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False)
