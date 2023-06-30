from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET-KEY']= 'secret'
sio = SocketIO(app)

@app.route('/')
def index ():
    return "hello"

@sio.event()
def send_msg(msg):
    print("MESSAGE" + msg)



if __name__ == '__main__':
    sio.run(app)
