import json
import requests
import os
import exceptions
import sys


class send_api_cloud():

    def post(json):
        URL= "/post"
       # headers = {"Content-Type": "application/json",}
        try:
             r = requests.post(URL, json)
             p = r.json()
             if p == "status : 400":
                 exceptions.Handler_Exceptions()
                 return "400"
             return p
        
        except Exception as error:
            exceptions.Handler_Exceptions(error)
            sys.exit() 
            
        
    def put(json):
        URL = "/put"

        try:
            r = requests.put(URL, json)
            p = r.json()
        except Exception as error:
            exceptions.Handler_Exceptions(str(error))
            sys.exit()
                


        
    
