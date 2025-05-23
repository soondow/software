import time
from .datastore import ORDERS
from .notifications import socketio

def barista_simulation(order_id):
    time.sleep(5)
    ORDERS[order_id]["status"] = "preparing"
    socketio.emit('order_status', {
        "orderId": order_id, "status": "preparing"
    }, room=order_id)

    time.sleep(5)
    ORDERS[order_id]["status"] = "completed"
    socketio.emit('order_status', {
        "orderId": order_id, "status": "completed"
    }, room=order_id)
