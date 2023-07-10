import socketio
try:
    sio = socketio.Client()
    sio.connect("http://146.190.117.97:8000" , auth={'token':'3egUxGRb1x2ekiHreBshswQpsEL0QsgOtSYcMYiiOoPx7PtU70EYpHdJ6vALOisb'})
    DATA = [{'method':'hola', 'data':{}, 'route':'socket'}]
except Exception as e:
    print(e)     
    

@sio.event
def connect_error(data):
    print(data)

@sio.event
def POST(data:dict):
    print(data)

@sio.on('POST')
def post(orders:dict) -> dict:
    print(orders)
     
@sio.on('welcome')
def connect(data):
    print(data + f' i connect')  


sio.wait()   