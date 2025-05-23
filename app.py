from flask import Flask
from .auth import auth_bp
from .menu import menu_bp
from .inventory import inventory_bp
from .orders import orders_bp
from .payment import payment_bp
from .notifications import socketio
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    # Blueprint 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payment_bp)
    return app

app = create_app()
socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
