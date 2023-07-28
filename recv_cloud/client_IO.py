import socketio
import requests
import json
try:
    http_session = requests.Session()
    http_session.verify = False
    sio = socketio.Client()
    sio.connect("http://www.api.geekcod.com:8000" , auth={'token':'3egUxGRb1x2ekiHreBshswQpsEL0QsgOtSYcMYiiOoPx7PtU70EYpHdJ6vALOisb'})
    DATA = [{'method':'hola', 'data':{}, 'route':'socket'}]
except Exception as e:
    print(e)     
    

@sio.event
def connect_error(data):
    print(data)

@sio.on('POST')
def post(orders:dict) -> dict:
    print(orders)
    if orders['type'] == 'order':
        nro_order = orders['data']['_id']
        with open("X:/a2appsH/Pagina_Web/ConectorA2/Orders_/" + nro_order + ".json", 'w') as json_order:
            json.dump(orders['data'], json_order, indent=4)
    if orders['type'] =='client':
        id_client = orders['data']['rif'] 
        with open("X:/a2appsH/Pagina_Web/ConectorA2/Orders_/" + id_client +".json", 'w') as json_client: 
         json.dump(orders, json_client, indent=4) 
           
@sio.on('welcome')
def connect(data):
    print(data + f' i connect') 
    sio.emit('sync')
# sio.emit('sync') 
# def sync(synco):
#         print("prueba")
#         print(synco)

sio.wait()   