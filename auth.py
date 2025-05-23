from flask import Blueprint, request, jsonify
import uuid
from .datastore import USERS, TOKENS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = data.get("username")
    pwd  = data.get("password")
    if USERS.get(user) == pwd:
        token = str(uuid.uuid4())
        TOKENS[token] = user
        return jsonify({"token": token}), 200
    return jsonify({"error": "잘못된 자격증명"}), 401

def authorize():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.split()[1]
        return TOKENS.get(token)
    return None
