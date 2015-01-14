#!flask/bin/python
from app import app, socketio
socketio.run(app)

# from socketio.server import SocketIOServer

# SocketIOServer(('', 5000), app, resource="socket.io").serve_forever()
