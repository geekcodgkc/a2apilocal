import json
import requests


class Request():

    def send_json(url, json):
       # headers = {"Content-Type": "application/json",}
        try:
             r = requests.post(url, json)
             p = r.json()
             return p
        
        except Exception as error: 
            return str(error)
        
    
