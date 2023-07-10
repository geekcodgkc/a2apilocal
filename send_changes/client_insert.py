import pyodbc
import json
import glob
import os
import sys
from exceptions import Handler_Exceptions
class client():

    def read_client_to_insert():
        list_jsons = glob.glob("C:/a2CA2020/Empre001/TMP/*.json")
        if len(list_jsons) > 0:
            list_str = str(list_jsons[0])
            file_json = list_str.replace("\\", "/")
            if os.stat(file_json).st_size != 0:  
                with open(file_json, mode="r") as file:
                    clients = json.load(file)
                    return clients
            else:
                print("Archivo vacio")
                sys.exit()
        else:
            sys.exit()        

    def search_client_if_exist(rif_client):
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute(f"SELECT FC_CODIGO FROM SCLIENTES WHERE FC_CODIGO = '{rif_client}'")
            var = cur.fetchall()
            if len(var) > 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def search_activated_client(rif_cliente):
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute(f"SELECT FC_CODIGO, FC_GKC_INTERNET FROM SCLIENTES WHERE FC_STATUS = 1 AND FC_GKC_INTERNET = 1 AND FC_CODIGO = '{rif_cliente}' ")
            var = cur.fetchall()
            for i in var:
                
                return
        except Exception as e:
            print(e)  

    def insert_client():
        read = client.read_client_to_insert()
        if_exist = client.search_client_if_exist(read['id'])
        if type(read) == dict and if_exist == False:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute("INSERT INTO (FC_CODIGO, FC_DESCRIPCION, FC_STATUS, FC_RIF, FC_DIRECCION1)")
        else:
            if type(read) == dict and if_exist == True:
                put = client.search_activated_client(read["id"])
                print("No hice nada")

ini = client.insert_client()