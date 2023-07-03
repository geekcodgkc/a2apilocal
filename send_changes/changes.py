import pyodbc
import json
import sys

#from function import send_api_cloud

class search_changes():

    def query_tb_temp():   
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur_a2 = connect.cursor()
            cur_a2.execute("""SELECT FIC_CODEITEM AS CODIGO,
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
                                    INTO TABLE_B
                                    FROM PRUEBA_INV
                                    INNER JOIN PRUEBA_COSTO  ON CODIGOINV = CODIGO
                                    INNER JOIN PRUEBA_EXI    ON CODIGOINV = CODIGO_EX
                                    """)
            

            cur_a2.execute("""CREATE INDEX "KEY_CODIGO" ON TABLE_B (CODIGOINV) """ )
        
            #print(json)
            connect.close()
            return 'Connection success'
        except Exception as e:
            connect.close()
            return str(e)

    def convert_tableB_toA():
        try:
           connect = pyodbc.connect("DSN=A2KSA")
           cur = connect.cursor()
           cur.execute("""SELECT *
                            INTO TABLE_A
                            FROM TABLE_B""")

        except Exception as e:
            print(e)   

    def search_new_register():
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute("""SELECT CODIGOINV, DESCRIPCION, PRECIOBS, PRECIOUS, PRECIOUS2, EXISTENCIA 
                            FROM TABLE_B B
                            LEFT JOIN TABLE_A A ON B.CODIGOINV = A.CODIGOINV
                            WHERE B.PRECIOUS <> A.PRECIOUS OR B.PRECIOUS2 <> A.PRECIOUS2 
                            OR B.EXISTENCIA <> A.EXISTENCIA 
                        """)    
            new = cur.fetchall()
            if len(new) > 0:
                json_new = {}
                json_new['data'] = []
                for i in new:
                    json_new['data'].append({'id_product': i[0],
                                                'description': i[1],
                                                'priceUS': i[3],
                                                'priceUS2': i[4],
                                                'ext': i[5]
                                                })
                print(json_new)    
                connect.close()
                return json_new
            else:
                connect.close()    
                return '200'    

        except Exception as e:
            print(e)      



    def search_update():
        ###SEARCHING UPDATES IN DATABASE######
        try:
            result = search_changes.query_tb_temp()
            connect = pyodbc.connect("DSN=A2KSA")
            cursor = connect.cursor()
            cursor.execute("""SELECT CODIGOINV, DESCRIPCION, PRECIOBS, PRECIOUS, PRECIOUS2, EXISTENCIA 
                            FROM TABLE_B B
                            RIGHT JOIN TABLE_A A ON B.CODIGOINV = A.CODIGOINV
                            WHERE B.PRECIOUS <> A.PRECIOUS OR B.PRECIOUS2 <> A.PRECIOUS2 
                            OR B.EXISTENCIA <> A.EXISTENCIA
                            """)
            table = cursor.fetchall()
            json_insert = search_changes.search_new_register()
            if len(table) > 0:
                json = {}
                json['data']= []
                for i in table:
                    json['data'].append({'id_product': i[0],
                                                'description': i[1],
                                                'priceUS': i[3],
                                                'priceUS2': i[4],
                                                'ext': i[5]
                                                })
                from function import send_api_cloud
                var_post = send_api_cloud.post(json)
                if var_post != '400':
                    search_changes.convert_tableB_toA()
                else:
                    sys.exit()    

                connect.close()     
            else: 
                connect.close()
                pass

            if json_insert == dict:
                from function import send_api_cloud
                send_api_cloud.post(json_insert)
            
        except Exception as e:
            connect.close()
            return str(e)


ini = search_changes.search_update()   
