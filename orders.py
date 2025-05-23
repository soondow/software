from flask import Blueprint, request, jsonify
import uuid
from .auth import authorize
from .datastore import MENU, INVENTORY, ORDERS
from .notifications import socketio

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/order/create', methods=['POST'])
def create_order():
    user = authorize()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    data     = request.json
    item     = data.get("item")
    qty      = int(data.get("qty", 1))
    amount   = MENU.get(item, 0) * qty
    order_id = str(uuid.uuid4())
    ORDERS[order_id] = {
        "user":   user,
        "item":   item,
        "qty":    qty,
        "amount": amount,
        "status": "created"
    }
    return jsonify({"orderId": order_id, "amount": amount}), 201

@orders_bp.route('/order/update', methods=['POST'])
def update_order():
    user = authorize()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    data     = request.json
    oid      = data.get("orderId")
    new_qty  = int(data.get("qty", 1))
    order    = ORDERS.get(oid)
    if not order or order["status"] != "created":
        return jsonify({"error": "수정 불가"}), 400
    if INVENTORY.get(order["item"], 0) < new_qty:
        return jsonify({"error": "재고 부족"}), 400

    order["qty"]    = new_qty
    order["amount"] = MENU[order["item"]] * new_qty
    return jsonify({"orderId": oid, "status": "updated"}), 200

@orders_bp.route('/order/cancel', methods=['POST'])
def cancel_order():
    user = authorize()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    oid   = request.json.get("orderId")
    order = ORDERS.get(oid)
    if not order or order["status"] not in ("created", "paid"):
        return jsonify({"error": "취소 불가"}), 400

    order["status"] = "cancelled"
    socketio.emit('order_status', {
        "orderId": oid, "status": "cancelled"
    }, room=oid)
    return jsonify({"orderId": oid, "status": "cancelled"}), 200
