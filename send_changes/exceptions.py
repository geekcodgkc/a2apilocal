import json
import datetime

class Handler_Exceptions():

    def write_fatal_exceptions(error):
        print(error)

    def save_json_to_put_send_client(file:dict, id_client:str):
        with open(f"//192.168.1.254/a2appsH$/Pagina_Web/ConectorA2/Handler_Errors/Clients_Errors/Put_Errors/{id_client}-PUT.json", "w") as save:
               json.dump(file, save, indent=4)

    def save_json_to_put_send_product(file:dict, id_product:str):
        with open(f"//192.168.1.254/a2appsH$/Pagina_Web/ConectorA2/Handler_Errors/Orders_Errors/Put_Errors/{id_product}-PUT.json", "w") as save:
               json.dump(file, save, indent=4)

    def save_json_to_post_send(file:dict):
         time = datetime.datetime.now().strftime('%Y%m%d%H%M')
         with open(f"C:/a2CA2020/Empre001/TMP/{time}POST.json",  "w") as save:
              json.dump(file, save, indent=4)    

            