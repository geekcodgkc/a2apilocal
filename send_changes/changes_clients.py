import os
import sys
import pyodbc
import requests
from exceptions import Handler_Exceptions
from import_env import search_env

class changes_customer():

    def compare_GKCtableA_B():
        """This function create two temporary table, to compare that tables and return a list if have
         found a change """
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute("""SELECT FC_CODIGO, FC_GKC_INTERNET
                                INTO "//192.168.1.254/a2appsH$/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEA"
                                FROM SCLIENTES
                            WHERE FC_STATUS = 1 """)
            cur.execute("""CREATE INDEX IF NOT EXISTS "FC_CODE" ON "//192.168.1.254/a2appsH$/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEA" ("FC_CODIGO") """)

            cur.execute("""SELECT FC_CODIGO, FC_GKC_INTERNET
                            FROM "//192.168.1.254/a2appsH$/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEA" A
                            INNER JOIN "//192.168.1.254/a2appsH$/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEB" B ON A.FC_CODIGO = B.FC_CODIGO
                            WHERE A.FC_GKC_INTERNET <> B.FC_GKC_INTERNET """)
            actualiza = cur.fetchall()
            if len(actualiza) > 0:
                return actualiza
            else:
                return False
            
        except Exception as e:
            print(str(e))
            return 'Error'  
          
    def put_changes():
        try:
            result = changes_customer.compare_GKCtableA_B()
            if type(result) == list:
                json_update = {}
                for i in result:
                    id = i[0]  
                    json_update.update({'status': i[1]})
                    env_ = search_env()
                    r = requests.put(env_[0] + f'/clients/{id}', headers=env_[1], json=json_update)
                    p = r.request
                    print(str(p))
                print(json_update)    
            else:
                print("NADA")
                sys.exit()        

        except Exception as e:
            Handler_Exceptions.save_json_to_put_send_client(json_update, id)
            print(e)    

init = changes_customer.put_changes()            