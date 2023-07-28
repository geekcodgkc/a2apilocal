import json
import requests
import os
from exceptions import Handler_Exceptions
import sys
from import_env import env

class send_api_cloud():

    def post(post):
        try:
             env_ = env.search_env()
             r = requests.post(env_[0]+ '/products',headers=env_[1] , json=post)
             p = r.json()
             a= r.elapsed
             print(a)
             if p == {"error":"hubo un error", "rawError":{}}:
                 Handler_Exceptions.save_json_to_post_send(post)
                 return "400"
             return p
        
        except Exception as error:
            Handler_Exceptions.save_json_to_post_send(post)
            return "400"
         
            
        
    def put(update):

        def prices(x):
            if x != -1 and x!= 0:
                return x
            else:
                if x == 0:
                    x= -2
                    return x
                return False
       
        try:
            env_ = env.search_env()
            for i in update:
                json_update = {}
                prices_list = filter(prices, i)
                if (i[3] != -1) or (i[4] != -1) or (i[5] != -1) or (i[6] != -1):
                    json_update.update({'prices': {}})
                    for x in prices_list:
                        if i[3] == x:
                            json_update['prices']['p1'] = i[3]
                    
                        if i[4] == x:
                            json_update['prices']['p2'] = i[4]
                    
                        if i[5] == x :
                            json_update['prices']['p3'] = i[5]
                    
                        if i[6] == x:
                            json_update['prices']['p4'] = i[6]
                if i[1] != '0':
                    json_update['name']= i[1]
                if i[2] != None:
                    json_update['status'] = i[2]                
                
                print(json_update) 
                try:    
                    if len(json_update) > 0:
                        r = requests.put(env_[0] + f'/products/{i[0]}',headers=env_[1] ,json=json_update)
                        if r.status_code == 400 and r.text != {'error': 'hubor un error',
                                                                'rawError': {}}:  
                            Handler_Exceptions.save_json_to_put_send_product(json_update, id_product=i[0])
                            return '400'
                    else:
                        pass
                except Exception as e: 
                     Handler_Exceptions.save_json_to_put_send_product(json_update, id_product= i[0])      
                     print(e)
                     return '400'  
        except Exception as error:
                    print(str(error))
                    Handler_Exceptions.save_json_to_put_send_product(json_update, id_product= i[0])
                    Handler_Exceptions.write_fatal_exceptions(str(error), "Products_Exceptions/Put_Exceptions/Fatal_Exceptions/exceptions_.txt")
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
                    


        
    
