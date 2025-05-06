from flask import Flask
from auth import auth

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
