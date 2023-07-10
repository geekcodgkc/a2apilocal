import requests
import json
import pyodbc
from function import send_api_cloud
from exceptions import Handler_Exceptions


class Api():
    def connect_database():
       try: 
            json_response ={}
            json_response['data'] = []

            a2_database = pyodbc.connect("DSN=A2KSA")
            cur_a2 = a2_database.cursor()
            cur_a2.execute("""SELECT
                                    FI_CODIGO,
                                    FI_DESCRIPCION,
                                    FI_REFERENCIA,
                                    FI_INTERNET,
                                    FI_UNIDAD,
                                    CAST(FI_CATEGORIA AS VARCHAR(8)) AS FI_CATEGORIA
                                    INTO "C:/a2CA2020/Empre001/TMP/A2INVENTARIO"
                                    FROM SINVENTARIO""")
            cur_a2.execute("""CREATE INDEX IF NOT EXISTS "FI_KEYCODIGO" ON "C:/a2CA2020/Empre001/TMP/A2INVENTARIO" ("FI_CODIGO")""")

            cur_a2.execute("""CREATE INDEX IF NOT EXISTS "FI_KEYDEP01" ON "C:/a2CA2020/Empre001/TMP/A2INVENTARIO" ("FI_CATEGORIA");""")
    
                
            cur_a2.execute("""SELECT 
                                FIC_CODEITEM,
                                FIC_P01PRECIOTOTALEXT,     --PRECIO 01 EN DOLARES.
                                FIC_P02PRECIOTOTALEXT,     --COSTO ACTUAL   EN DOLARES.
                                FIC_P03PRECIOTOTALEXT,     --COSTO PROMEDIO EN DOLARES.
                                FIC_P04PRECIOTOTALEXT
                                INTO "C:/a2CA2020/Empre001/TMP/A2PRECIOS"
                                FROM A2INVCOSTOSPRECIOS """)
            cur_a2.execute("""CREATE INDEX IF NOT EXISTS "FIC_CODEITEM" ON "C:/a2CA2020/Empre001/TMP/A2PRECIOS" ("FIC_CODEITEM")""") 

            cur_a2.execute("""SELECT 
                                FD_CODIGO,
                                FD_DESCRIPCION
                                INTO "C:/a2CA2020/Empre001/TMP/A2DEP01"
                                FROM SCATEGORIA
                                """)
                
            cur_a2.execute("""CREATE INDEX IF NOT EXISTS "FD_KEYCODIGO" ON "C:/a2CA2020/Empre001/TMP/A2DEP01"  ("FD_CODIGO") """)

            cur_a2.execute("""SELECT
                                FT_CODIGOPRODUCTO,
                                SUM(FT_EXISTENCIA) AS EXISTENCIA
                                INTO "C:/a2CA2020/Empre001/TMP/A2EXISTENCIA"
                                FROM SINVDEP
                                GROUP BY FT_CODIGOPRODUCTO
                                    """)
            cur_a2.execute("""CREATE INDEX IF NOT EXISTS "FD_KEYCODIGO" ON "C:/a2CA2020/Empre001/TMP/A2EXISTENCIA" ("FT_CODIGOPRODUCTO") """ )
            ##########CREATING TABLE A FIRST TIME EVER###############################
            cur_a2.execute("""SELECT
                                    FI_CODIGO,
                                    FI_DESCRIPCION,
                                    FI_REFERENCIA,
                                    FI_INTERNET,
                                    FI_CATEGORIA,
            

                                    FIC_P01PRECIOTOTALEXT AS PRECIO01,     
                                    FIC_P02PRECIOTOTALEXT AS PRECIO02,     
                                    FIC_P03PRECIOTOTALEXT AS PRECIO03,     
                                    FIC_P04PRECIOTOTALEXT AS PRECIO04,
                                    FI_UNIDAD

                                    INTO "C:/a2CA2020/Empre001/TMP/TABLA_A "
                                    FROM "C:/a2CA2020/Empre001/TMP/A2INVENTARIO" 
                                    INNER JOIN "C:/a2CA2020/Empre001/TMP/A2PRECIOS" ON FI_CODIGO = FIC_CODEITEM""")
                                    #INNER JOIN "C:/a2CA2020/Empre001/TMP/A2DEP01"  ON FI_CATEGORIA = FD_CODIGO
                                    ##INNER JOIN "C:/a2CA2020/Empre001/TMP/A2EXISTENCIA" ON FI_CODIGO = FT_CODIGOPRODUCTO """)
            ######### QUERY TO SEND PRODUCTS TO WEB FIRST TIME EVER WHEN FI_INTERNET = TRUE####################
            cur_a2.execute("""SELECT * FROM "C:/a2CA2020/Empre001/TMP/TABLA_A"  WHERE FI_INTERNET = 1 """)
            
            true =cur_a2.fetchall()
            cur_a2.execute("""SELECT * INTO "C:/a2CA2020/Empre001/TMP/TABLA_B" FROM "C:/a2CA2020/Empre001/TMP/TABLA_A" """)
            a2_database.close()
            print(len(true))
            return true
       except Exception as e:
               print(e)
               return str(e)

    def post_firs_time():
        list_products = Api.connect_database()
        json_array = []
        for i in list_products:
             json_array.append({'id': i[0],
                                   'name': i[1],
                                   'prices': {'p1': i[5],
                                                'p2': i[6],
                                                'p3':i[7],
                                                'p4':i[8] },
                                   'presentation': 'botella'
                                                } )
        Handler_Exceptions.save_json_to_post_send(json_array)         
        status = send_api_cloud.post(json_array)   
        print(status)  

ini = Api.post_firs_time()      