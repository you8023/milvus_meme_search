from flask import Flask
from . import meme_ops

def create_app():
    app = Flask(__name__)

    app.register_blueprint(meme_ops.bp)

    return app