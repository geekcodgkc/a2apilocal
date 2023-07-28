import json
import datetime

class Handler_Exceptions():

    def write_fatal_exceptions(error, path):
        time = datetime.datetime.now().strftime('%Y%m%d%H%M')
        with open("X:/a2appsH/Pagina_Web/ConectorA2/Handler_Exceptions/"+ f"{path}", "a") as file:
             file.writelines(f"{time}:"+f'[{error}]' +"\n")
            
    def save_json_to_put_send_client(file:dict, id_client:str):
        with open(f"X:/a2appsH/Pagina_Web/ConectorA2/Handler_Exceptions/Clients_Exceptions/Put_Exceptions/{id_client}.json", "a") as save:
               json.dump(file, save, indent=4)

    def save_json_to_put_send_product(file:dict, id_product:str):
        with open(f"X:/a2appsH/Pagina_Web/ConectorA2/Handler_Exceptions/Orders_Errors/Put_Exceptions/{id_product}.json", "a") as save:
               json.dump(file, save, indent=4)

    def save_json_to_post_send(file:dict):
         time = datetime.datetime.now().strftime('%Y%m%d%H%M')
         with open(f"X:/a2appsH/Pagina_Web/ConectorA2/Handler_Exceptions/Products_Exceptions/Post_Exceptions/{time}POST.json",  "a") as save:
              json.dump(file, save, indent=4)    

            