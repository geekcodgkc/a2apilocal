import json

class Handler_Exceptions():

    def write_fatal_exceptions(error):
        print(error)

    def save_json_to_put_send(file:dict, id_product:str):
        with open(f"C:/a2CA2020/Empre001/TMP/{id_product}.json", "w") as save:
               json.dump(file, save, indent=4)
