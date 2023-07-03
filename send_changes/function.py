import json
import requests
import pymongo
import os


class send_api_cloud():

    def post(json):
        URL= "/post"
       # headers = {"Content-Type": "application/json",}
        try:
             r = requests.post(URL, json)
             p = r.json()
             return p
        
        except Exception as error: 
            return str(error)
        
   
        
    
