from flask import Blueprint, request, jsonify
from .auth import authorize
from .datastore import INVENTORY

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory/check', methods=['POST'])
def check_inventory():
    if not authorize():
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    item = data.get("item")
    qty  = int(data.get("qty", 1))
    if INVENTORY.get(item, 0) >= qty:
        return jsonify({"ok": True}), 200
    return jsonify({"ok": False, "error": "재고 부족"}), 400
