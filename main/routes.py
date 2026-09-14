import os
from main import app
from flask import request, flash, redirect, render_template


from main.form import EncodeForm, DecodeForm
from werkzeug.utils import secure_filename
from settings import ENCODE_INPUT_DIR, ENCODE_OUTPUT_DIR, DECODE_INPUT_DIR, DECODE_OUTPUT_DIR

def check_image_path():
    if not os.path.exists(os.path.join(app.root_path, "images")):
        os.mkdir(os.path.join(app.root_path, "images"))
    for directory in (ENCODE_INPUT_DIR, ENCODE_OUTPUT_DIR, DECODE_INPUT_DIR, DECODE_OUTPUT_DIR):
        os.makedirs(directory, exist_ok=True)

check_image_path()

@app.route("/", methods=["GET", "POST"])
def home():
    form = EncodeForm(request.form)
    deform = DecodeForm(request.form)
    return render_template("base.html", encode_form=form, decode_form = deform)

@app.route("/decode")
def decode_image():
    form = DecodeForm
    return render_template('decode.html', form=form, title = 'Decode Form' )


@app.route('/encode-image', methods=['POST'])
def encode():
    
    data = request.form

    f = request.files.get('file')
    img_path = f'main/static/image/temp/encode/{f.filename}'
    f.save(img_path)
    client_id = data.get("client_id")
    payload_message  = data.get("message")
    payload_file = request.files.get('message_file')
   
    if payload_message:
        print(payload_message)
        from service.tasks import encode_text_on_image
        encode_text_on_image.delay(img_path, payload_message, client_id)
        return {"status": "Success"}, 201
    if payload_file:
        from service.tasks import encode_image_on_image
        payload_file_path = f'main/static/image/temp/encode/{payload_file.filename}'
        payload_file.save(payload_file_path)
        encode_image_on_image.delay(img_path, payload_file_path, client_id)
        return {"status": "Sucess"}, 201
