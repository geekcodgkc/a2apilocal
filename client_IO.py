import socketio

sio = socketio.Client()


@sio.event(namespace='/')
def send_msg():
     sio.emit("send_msg", "he", namespace="/")
     print("send hello")

sio.connect("http://localhost:5000")
   