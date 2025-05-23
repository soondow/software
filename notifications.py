from flask_socketio import SocketIO, join_room

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('join')
def handle_join(data):
    room = data.get("orderId")
    join_room(room)
