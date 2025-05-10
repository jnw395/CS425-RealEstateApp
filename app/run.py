from flask import Flask
from auth import auth
from dotenv import load_dotenv
import os




def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    app.register_blueprint(auth)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
