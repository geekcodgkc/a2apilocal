import json
import datetime

class Handler_Exceptions():

    def write_fatal_exceptions(error):
        print(error)

    def save_json_to_put_send(file:dict, id_product_orclient:str):
        with open(f"C:/a2CA2020/Empre001/TMP/{id_product_orclient}-PUT.json", "w") as save:
               json.dump(file, save, indent=4)

    def save_json_to_post_send(file:dict, name = 'POST'):
         time = datetime.datetime.now().strftime('%Y%m%d%H%M')
         with open(f"C:/a2CA2020/Empre001/TMP/{time}POST.json",  "w") as save:
              json.dump(file, save, indent=4)    

            