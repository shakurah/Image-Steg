import os
from flask_socketio import emit, SocketIO
from flask import url_for
from settings import SOCKET_IO_MESSAGING_QUEUE, ENCODE_OUTPUT_DIR

from service import worker
from steg.algo import ImageParser, Format
from main import app

print("SOCKETIO QUEUE (celery process sees):", SOCKET_IO_MESSAGING_QUEUE)
socketio = SocketIO(message_queue=SOCKET_IO_MESSAGING_QUEUE)
try:
    socketio.emit("test-event", {"msg": "celery worker startup test"})
    print("TEST EMIT: sent without raising an exception")
except Exception as e:
    print("TEST EMIT FAILED:", repr(e))


@worker.task
def encode_text_on_image(img_path, text, client_id):
    with app.app_context(), app.test_request_context():
        img = ImageParser(img_path)

        for prog in img.encode(
            Format.TXT.value, text, as_generator=True,
        ):
            socketio.emit("encode:progress", {"progress": prog}, to=client_id)

        filename = os.path.basename(img_path)[: img_path.find(".")]

        encoded_image_url = url_for("static", filename=filename, _external=True)

        socketio.emit("encode:complete", {"data": encoded_image_url}, to=client_id)


@worker.task
def encode_image_on_image(img_path, img, client_id):
    with app.app_context(), app.test_request_context(base_url="http://localhost:5050/"):
        base_img = ImageParser(img_path)

        ext = os.path.splitext(img)[-1].lower()
        image_format = (
            Format.JPG.value if ext == "jpg" or ext == "jpeg" else Format.PNG.value
        )

        for prog in base_img.encode(
            image_format, img, as_generator=True, output_dir="static"
        ):
            socketio.emit("encode:progress", {"progress": prog}, to=client_id)

        name_no_ext = os.path.splitext(os.path.basename(img_path))[0]
        encoded_filename = f"encoded-{name_no_ext}.png"
        static_relative_dir = os.path.relpath(os.path.abspath(ENCODE_OUTPUT_DIR), app.static_folder)
        static_relative_path = os.path.join(static_relative_dir, encoded_filename).replace(os.sep, "/")
        encoded_image_url = url_for("static", filename=static_relative_path, _external=True)
        
        socketio.emit("encode:complete", {"data": encoded_image_url}, to=client_id)


@worker.task
def encode_audio_on_image(img_path, audio_file, client_id):
    with app.app_context():
        img = ImageParser(img_path)

        ext = os.path.splitext(audio_file)[-1].lower()
        image_format = Format.WAV.value if ext == "wav" else Format.MP3.value

        for prog in img.encode(
            image_format, audio_file, as_generator=True, output_dir="static"
        ):
            socketio.emit("encode:progress", {"progress": prog}, to=client_id)

        filename = os.path.basename(img_path)[: img_path.find(".")]

        encoded_image_url = url_for("static", filename=filename, _external=True)

        socketio.emit("encode:complete", {"data": encoded_image_url}, to=client_id)

