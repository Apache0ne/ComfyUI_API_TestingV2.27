from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'your_secret_key_here'

    from app import routes
    app.register_blueprint(routes.bp)

    return app