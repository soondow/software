from flask import Blueprint, jsonify
from .auth import authorize
from .datastore import MENU

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    if not authorize():
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(MENU), 200
