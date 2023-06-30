import requests
import json
import pyodbc
from function import Request as req

class Api():

    def pull_request():
        url = "****"
        acces_token = "****"
        headers = {""}
        body = {""}

        r = requests.post(url, )

    def connect_database():
       try: 
            json_response ={}
            json_response['data'] = []

            a2_database = pyodbc.connect("DSN=A2KSA")
            cur_a2 = a2_database.cursor()
            cur_a2.execute("""SELECT 
                                    FIC_CODEITEM AS CODIGO,
                                    FIC_P01IPRECIOTOTAL AS PRECIOBS,
                                    FIC_P01PRECIOTOTALEXT * 1.16 AS PRECIOUS,
                                    FIC_P02IPRECIOTOTAL AS PRECIOBS2,
                                    FIC_P02PRECIOTOTALEXT * 1.16 AS PRECIOUS2
                                    INTO PRUEBA_COSTO
                                    FROM A2INVCOSTOSPRECIOS""")
            cur_a2.execute("""CREATE INDEX "KEY_CODIGO" ON PRUEBA_COSTO (CODIGO) """)
            
            cur_a2.execute("""SELECT 
                                    FI_CODIGO AS CODIGOINV,
                                    FI_DESCRIPCION AS DESCRIPCION,
                                    FI_CATEGORIA
                                INTO PRUEBA_INV
                                FROM SINVENTARIO
                                WHERE FI_STATUS = 1 """)
            cur_a2.execute("""CREATE INDEX "KEY_CODIGO" ON PRUEBA_INV (CODIGOINV)""") 

            cur_a2.execute("""SELECT 
                                    FT_CODIGOPRODUCTO AS CODIGO_EX,
                                    FT_CODIGODEPOSITO AS DEPOSITO,
                                    CASE WHEN (FT_EXISTENCIAPEDIDO = NULL) AND (FT_EXISTENCIA = NULL) THEN 0
                                         WHEN (FT_EXISTENCIAPEDIDO = NULL) AND (FT_EXISTENCIA >= 0) THEN FT_EXISTENCIA
                                         WHEN (FT_EXISTENCIAPEDIDO = NULL) AND (FT_EXISTENCIA < 0) THEN FT_EXISTENCIA
                                    ELSE (FT_EXISTENCIA - FT_EXISTENCIAPEDIDO)
                                    END AS EXISTENCIA      
                                    INTO PRUEBA_EXI
                                FROM SINVDEP 
                                WHERE FT_CODIGODEPOSITO  = 2 
                                    """)
            
            cur_a2.execute("""CREATE INDEX "KEY_CODIGO" ON PRUEBA_EXI (CODIGO_EX) """)
            

            cur_a2.execute("""SELECT 
                                    CODIGOINV, DESCRIPCION, PRECIOBS, PRECIOBS2, PRECIOUS, PRECIOUS2, EXISTENCIA
                                INTO TABLE_A 
                                FROM PRUEBA_INV
                                INNER JOIN PRUEBA_COSTO  ON CODIGOINV = CODIGO
                                INNER JOIN PRUEBA_EXI    ON CODIGOINV = CODIGO_EX
                                 
                                """)
            cur_a2.execute("""CREATE INDEX "KEY_CODIGO" ON TABLE_A (CODIGOINV) """)
            
            lista = cur_a2.fetchall()
            
            #####DROP TABLE########
           # cur_a2.execute("DROP TABLE IF EXISTS PRUEBA_COSTO")
            #cur_a2.execute("DROP TABLE IF EXISTS PRUEBA_INV")
            #cur_a2.execute("DROP TABLE IF EXISTS PRUEBA_EXI")
            ######JSON TRANSFORM######

            for i in lista:
                #print(i[0])
                json_response["data"].append({'id_product': i[0],
                                              'description': i[1],
                                              'priceUS': i[4],
                                              'priceUS2': i[5],
                                              'ext': i[6]
                                              })
                #print(json_response)

            with open("C:\ApiRestFlask\PROYECTOS MEJORADOS\CONECTORPE\data1", "w") as g:
                  json.dump(json_response, g , indent=4)  

           # response = req.send_json("http://localhost:5000/", json_response)
            #print(response)

            
       except Exception as e:
               return str(e)
       

prueba = Api.connect_database()      