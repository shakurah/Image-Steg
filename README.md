# Image-Steg

Image-Steg is a web-based image steganography application that allows users to encode data into images and later decode the hidden data.

The project combines pixel-level image manipulation with asynchronous task processing and real-time communication to provide a complete web application rather than just a standalone steganography script.

## Live Demo

https://image-steg.onrender.com/

## Source Code

https://github.com/shakurah/Image-Steg

## Features

- Encode data into images using pixel-level manipulation
- Decode hidden data from encoded images
- Image upload and generated-file handling
- Background processing with Celery
- RabbitMQ message broker for asynchronous tasks
- Real-time communication using Flask-SocketIO
- Gevent-based asynchronous networking
- Docker-based RabbitMQ development environment
- Production deployment on Render

## How It Works

Image-Steg uses image steganography to hide information inside an image.

### Encoding

The application receives an image and the data that should be hidden. The data is converted into a form that can be embedded into the image's pixel data.

The application then modifies selected pixel information to store the data while keeping the resulting image visually similar to the original.

The encoded image can then be downloaded and used as the carrier for the hidden data.

### Decoding

When an encoded image is provided, the application reads the relevant pixel data and extracts the information that was previously embedded.

The extracted data is then returned to the user.

## Architecture

The application consists of several components:

- **Flask** handles the web application and HTTP requests.
- **Flask-SocketIO** provides real-time communication between the browser and server.
- **Celery** handles background/asynchronous tasks.
- **RabbitMQ** acts as the message broker used by Celery.
- **Gevent** provides the asynchronous networking layer.
- **Steganography logic** handles the encoding and decoding of data within images.

