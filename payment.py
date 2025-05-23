from flask import Blueprint, request, jsonify
from .auth import authorize
from .datastore import ORDERS
from .barista import barista_simulation
from .notifications import socketio
import threading

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment/process', methods=['POST'])
def process_payment():
    user = authorize()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data     = request.json
    oid      = data.get("orderId")
    card_no  = data.get("paymentInfo", {}).get("cardNumber", "")
    approved = not card_no.endswith("0")

    if approved:
        ORDERS[oid]["status"] = "paid"
        socketio.emit('order_status', {
            "orderId": oid, "status": "paid"
        }, room=oid)
        # 바리스타 준비 시뮬레이션
        threading.Thread(target=barista_simulation, args=(oid,), daemon=True).start()
        return jsonify({"status": "approved"}), 200

    return jsonify({"status": "declined"}), 400
