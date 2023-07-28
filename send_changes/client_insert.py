import pyodbc
import json
import glob
import os
import sys
import shutil
import requests
from import_env  import env 
from exceptions import Handler_Exceptions

class client():
    def read_client_to_insert():
        """Function search a new file return by socket in a
        folder and return if exist a json file and construct Table after validate not exists json file exceptions 
        """
        put_exceptions = glob.glob("X:/Pagina_Web/ConectorA2/Handler_Exceptions/Clients_Exceptions/Put_Exceptions/*.json")
        if len(put_exceptions) == 0:
            try:
                connect = pyodbc.connect("DSN=A2KSA")
                cur = connect.cursor()
                cur.execute("""SELECT FC_CODIGO, FC_GKC_INTERNET
                                INTO "X:/a2appsH/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEB"
                                FROM SCLIENTES
                            WHERE FC_STATUS = 1 """)
                cur.execute("""CREATE INDEX IF NOT EXISTS "FC_CODE" ON "X:/a2appsH/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEB" ("FC_CODIGO") """)
                connect.close()
            except Exception as e:
                Handler_Exceptions.write_fatal_exceptions(str(e), "Clients_Exceptions/Dbisam_Exceptions/errorDbisam.txt")
                pass
        else:        
            pass    
        list_jsons = glob.glob("X:/a2appsH/Pagina_Web/ConectorA2/Json__File/NewClients/*.json")
        if len(list_jsons) > 0:
            list_str = str(list_jsons[0])
            file_json = list_str.replace("\\", "/")
            if os.stat(file_json).st_size > 0:  
                with open(file_json, mode="r") as file:
                    clients = json.load(file)
                    print('test 1')
                    return clients, file_json
            else:
                print("Archivo vacio")
                sys.exit()
        else:
            os._exit(0)
            sys.exit()    

    def search_client_if_exist(rif_client):
        """Verifiying the client exists in a2 database"""
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute(f"SELECT FC_CODIGO FROM SCLIENTES WHERE FC_CODIGO = '{rif_client['id']}'")
            var = cur.fetchall()
            if len(var) > 0:
                print('test2')
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def search_activated_client(client):
        """VERIFIYING THE CLIENT IS ACTIVATED IN A2 DATABASE
        """
        try:
            json_update_client = {}
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute(f"SELECT FC_CODIGO, FC_GKC_INTERNET FROM SCLIENTES WHERE FC_STATUS = 1 AND FC_GKC_INTERNET = 1 AND FC_CODIGO = '{client['id']}' ")
            var = cur.fetchall()
            if len(var) > 0:
                for i in var:
                    json_update_client.update({'verified': True})
                    print('pass3')
                    return json_update_client
            else:
                return None    
        except Exception as e:
            print(e)
            return None  
    
    def move_file(path_file):
        """Move json file to new path only if the put method was 'OK' """
        move = shutil.move(path_file, "X:/a2appsH/Pagina_Web/ConectorA2/Json__File/NewClients/ProccesJson")
        print(str(move))


    def insert_client():
        """Father function to start the program script and every function called"""
        read = client.read_client_to_insert()
        if_exist = client.search_client_if_exist(read[0])
        if type(read[0]) == dict and if_exist == False:
            try:
                index_client = read[0]
                connect = pyodbc.connect("DSN=A2KSA")
                cur = connect.cursor()
                count_columns = cur.execute(f"""INSERT INTO SCLIENTES (FC_CODIGO, FC_DESCRIPCION, FC_STATUS, FC_RIF, FC_DIRECCION1)
                        VALUES('{index_client['id']}', '{index_client['name']}', 1, '{index_client['id']}', '{index_client['address']}')""")
                print(count_columns)
                client.move_file(read[1])
                cur.commit()
                
               
            except Exception as e:
                print(e)
                sys.exit()    
        else:
            try:
                if type(read[0]) == dict and if_exist == True:
                    put = client.search_activated_client(read[0])
                    if put == None:
                        client.move_file(read[1])
                        os._exit(0)
                    else:    
                        id = read[0]
                        path = read[1]
                        try:
                            env_=env.search_env()
                            r = requests.put(env_[0] + f"/clients/{id['id']}", headers=env_[1], json= put)
                            p = r.json()
                            r.status_code
                            client.move_file(path)
                        except Exception as e:
                            Handler_Exceptions.save_json_to_put_send_client(put, id['id'])
                            print(e)
                    
                    print(put)
                    print("No hice nada")
            except Exception as e:
                print(e)   

ini = client.insert_client()  