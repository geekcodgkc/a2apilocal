import os
import sys
import pyodbc
import requests
from exceptions import Handler_Exceptions
from import_env import env

class changes_customer():

    def compare_GKCtableA_B():
        """This function create two temporary table, to compare that tables and return a list if have
         found a change """
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute("""SELECT FC_CODIGO, FC_GKC_INTERNET
                                INTO "X:/a2appsH/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEA"
                                FROM SCLIENTES
                            WHERE FC_STATUS = 1 """)
            cur.execute("""CREATE INDEX IF NOT EXISTS "FC_CODE" ON "X:/a2appsH/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEA" ("FC_CODIGO") """)

            cur.execute("""SELECT FC_CODIGO, FC_GKC_INTERNET
                            FROM "X:/a2appsH/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEA" A
                            INNER JOIN "X:/a2appsH/Pagina_Web/ConectorA2/Clients_/Tmp_clients/GKC_TABLEB" B ON A.FC_CODIGO = B.FC_CODIGO
                            WHERE A.FC_GKC_INTERNET <> B.FC_GKC_INTERNET """)
            actualiza = cur.fetchall()
            if len(actualiza) > 0:
                return actualiza
            else:
                return False
            
        except Exception as e:
            Handler_Exceptions.write_fatal_exceptions(str(e), "Clients_Exceptions/Dbisam_Exceptions/errorDbisam.txt")
            sys.exit(0)
          
    def put_changes():
        try:
           
            result = changes_customer.compare_GKCtableA_B()
            if type(result) == list:
                json_update = {}
                try:
                    for i in result:
                        id = i[0]  
                        json_update.update({'verified': i[1]})
                        env_ = env.search_env()
                        r = requests.put(env_[0] + f'/clients/{id}', headers=env_[1], json=json_update)
                        if r.status_code == 200 and r.text != 'null':
                                print("ACtualizado")
                                sys.exit
                        else:    
                            Handler_Exceptions.save_json_to_put_send_client(json_update, id)   
                       
                    print(json_update) 
                except Exception as e:
                    Handler_Exceptions.save_json_to_put_send_client(json_update, id['id'])       
            else:
                sys.exit(0)       

        except Exception as e:
            Handler_Exceptions.write_fatal_exceptions(e)
            print(e)    

init = changes_customer.put_changes()            