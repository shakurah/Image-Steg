from gevent import monkey
monkey.patch_all()
import os
from main import io, app
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    io.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
