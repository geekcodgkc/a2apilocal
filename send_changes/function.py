import json
import requests
import os
from exceptions import Handler_Exceptions
import sys
from dotenv import load_dotenv

load_dotenv("C:/ApiRestFlask/PROYECTOS MEJORADOS/CONECTORPE/.env.txt")
token = os.getenv('API_TOKEN')
URL = os.getenv('API_URL')
HEADERS = {'Authorization' : f'Bearer {token}'}

class send_api_cloud():
    global HEADERS
    global URL    
        

    def post(post):
        
                  #   "Content-Type" : "application/json"}
        try:
             r = requests.post(URL+ '/products', headers=HEADERS , json=post)
             p = r.json()
             a= r.elapsed
             print(a)
             if p == {'error':'hubo un error'}:
                 Handler_Exceptions.write_fatal_exceptions(p)
                 return "400"
             return p
        
        except Exception as error:
            Handler_Exceptions.write_fatal_exceptions(str(error))
            return "E400"
            sys.exit() 
            
        
    def put(update):
        URL = "http://200.8.121.68:3001/products"
        
        p1 = 'True'
        p2 = 'True'
        p3 = 'True'
        p4 = 'True'
        
        try:
            for i in update:
                json_update = {}
                if i[1] != '0':    
                    json_update.update({'name': i[1]})
                else:
                    pass
                if i[3] != -1:
                    json_update.update({'prices':{'p1': i[3]}})
                else:
                    p1 = 'False'
                    pass
                if i[4] != -1 and p1 == 'True':
                    p1 = 'True'
                    json_update.update({'prices':{'p1':i[3], 'p2': i[4]}})
                else:
                     if i[4] != -1 and p1 == 'False':
                        json_update.update({'prices':{'p2':i[4]}})
                        p2= 'True'
                     else: 
                         p2 = 'False'                   
                if i[5] != -1 and p1 == 'True' and p2 == 'True':
                    json_update.update({'prices':{'p1':i[3], 'p2': i[4], 'p3': i[5]}})
                else:
                     if i[5] != -1 and p2 == 'False' and p1 == 'False':
                        json_update.update({'prices':{'p3':i[5]}})
                        p3 = 'True'
                     elif i[5] != -1 and p1 == 'True':  
                            json_update.update({'prices': {'p1':i[3], 'p3':i[5]}})
                            p3 = 'True'
                     elif i [5] != -1 and p2 == 'True':
                            json_update.update({'prices': {'p2':i[4], 'p3':i[5]}})
                            p3 = 'True'  
                     else:
                         p3 = 'False'            
                if i[6] != -1 and json_update['prices'] == {'p1': i[3], 'p2': i[4], 'p3': i[5]}:
                    json_update.update({'prices':{'p1':i[3], 'p2': i[4], 'p3': i[5], 'p4': i[6]}})
                    p4 = 'True'
                else:
                    if i[6] != -1 and p2 == 'False' and p3 == 'False' and p1 == 'False':
                        json_update.update({'prices':{'p4':i[6]}})
                        p4= 'True'
                    elif i[6] != -1  and p1 == 'True':
                         json_update.update({'prices':{'p1': i[3], 'p4': i[6]}})
                         p4= 'True'
                    elif i[6] != -1 and p2  == 'True':     
                          json_update.update({'prices':{'p2': i[4], 'p4': i[6]}})
                          p4= 'True'
                    elif i[6] != -1 and p3  == 'True':    
                         json_update.update({'prices':{'p3': i[5], 'p4': i[6]}})
                         p4= 'True'
                    else:
                        p4= False
                if i[2] != None:
                        json_update.update({'status': i[2]})
                else:
                     pass                     
                print(json_update) 
                try:    
                    if len(json_update) > 0:
                        r = requests.put(URL + f'/{i[0]}', json=json_update)
                        p = r.json()
                        print(p)
                    else:
                        pass
                except Exception as e: 
                     Handler_Exceptions.save_json_to_put_send(json_update, id_product= i[0])      
                     print(e)
                     return '400'  
        except Exception as error:
                    print(str(error))
                    Handler_Exceptions.write_fatal_exceptions(str(error))
                    sys.exit()


    def inactivate(json, code):
        URL = "http://200.8.121.68:3001/products"
        try:
            r = requests.put(URL + f'/{code}', json=json)
            p = r.json()
            print(p)
            if p['id'] != code:
                 Handler_Exceptions.write_fatal_exceptions(p)
            else:
                 return '200'     
        except Exception as error:
            Handler_Exceptions.write_fatal_exceptions(str(error))
            sys.exit()    
                    


        
    
