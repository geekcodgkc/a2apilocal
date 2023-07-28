from dotenv import load_dotenv
import os

class env():

    def search_env():
        load_dotenv("X:/a2appsH/Pagina_Web/ConectorA2/_env/.env.txt")
        token = os.getenv('API_TOKEN')
        URL = os.getenv('API_URL')
        HEADERS = {'Authorization' : f'Bearer {token}'}
        return (URL, HEADERS)
        print(token)
