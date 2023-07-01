import json
import requests
import pymongo


class send_api_cloud():

    def send_json(url, json):
       # headers = {"Content-Type": "application/json",}
        try:
             r = requests.post(url, json)
             p = r.json()
             return p
        
        except Exception as error: 
            return str(error)
        
    
