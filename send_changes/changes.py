import pyodbc
import requests
import json
from function import send_api_cloud

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
            
    
    def deleted_table():
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute("""DROP TABLE IF EXISTS TABLE_A """)
            cur.execute("""DROP TABLE IF EXISTS TABLE_B""")
            connect.close()
        except Exception as e:
                connect.close()
                return str(e)

    def compare_db():
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
                connect.close()
                try:  
                    send_api_cloud.send_json()
                    search_changes.deleted_table()
                except Exception as error:
                    print(str(error))         
                
                return json 
            else: 
                connect.close()
                pass
            
        except Exception as e:
            connect.close()
            return str(e)


ini = search_changes.compare_db()   
