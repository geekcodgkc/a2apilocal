import pyodbc
import json
import sys
from function import send_api_cloud

#from function import send_api_cloud

class search_changes():

    def query_tb_temp():   
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur_a2 = connect.cursor()
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
                                FIC_P01PRECIOTOTALEXT,     
                                FIC_P02PRECIOTOTALEXT,     
                                FIC_P03PRECIOTOTALEXT,     
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
                
            cur_a2.execute("""CREATE INDEX IF NOT EXISTS "FD_KEYCODIGO" ON "C:/a2CA2020/Empre001/TMP/A2DEP01" ("FD_CODIGO")""")

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

                                    INTO "C:/a2CA2020/Empre001/TMP/TABLA_A" 
                                    FROM "C:/a2CA2020/Empre001/TMP/A2INVENTARIO" 
                                    INNER JOIN "C:/a2CA2020/Empre001/TMP/A2PRECIOS" ON FI_CODIGO = FIC_CODEITEM """)
                                    #INNER JOIN "C:/a2CA2020/Empre001/TMP/A2DEP01"  ON FI_CATEGORIA = FD_CODIGO
                                    #INNER JOIN "C:/a2CA2020/Empre001/TMP/A2EXISTENCIA" ON FI_CODIGO = FT_CODIGOPRODUCTO """)
            ######### QUERY TO SEND PRODUCTS TO WEB FIRST TIME EVER WHEN FI_INTERNET = TRUE####################
            #cur_a2.execute("""SELECT * FROM "C:/a2CA2020/Empre001/TMP/TABLA_A"  WHERE FI_INTERNET = 1 """)
        
            #print(json)
            connect.close()
            return 'Connection success'
        except Exception as e:
            connect.close()
            return str(e)

    def convert_tableA_toB():
        try:
           connect = pyodbc.connect("DSN=A2KSA")
           cur = connect.cursor()
           cur.execute("""SELECT *
                            INTO TABLA_B
                            FROM TABLA_A""")

        except Exception as e:
            print(e)   

    def changes_clients():
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute(""" """)
        except Exception as e:
            print(e)     

    def search_new_register():
        try:
            ##### SEARCH NEW PRODUCTS ACTIVATE AND CONSTRUCT JSON FILE TO POST METHOD ###########
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute("""SELECT * FROM "C:/a2CA2020/Empre001/TMP/TABLA_A" A
                                    WHERE FI_INTERNET = 1 AND FI_CODIGO NOT IN(SELECT FI_CODIGO FROM "C:/a2CA2020/Empre001/TMP/TABLA_B") 
                                                    """)    
            new = cur.fetchall()
            if len(new) > 0:
                json_array =  []
                for i in new:
                    
                    json_array.append({'id': i[0],
                                   'name': i[1],
                                   'prices': {'p1': i[5],
                                                'p2': i[6],
                                                'p3':i[7],
                                                'p4':i[8] },
                                   'presentation': i[9]
                                                } )
                connect.close()
                print(json_array)
                return json_array
            else:
                connect.close()    
                return '200'    

        except Exception as e:
            print(e)      
            return 'Database Error'


    def search_update():
        UPDATE = False
        NEW_PRODUCTS = False
        ###SEARCHING UPDATES IN DATABASE######
        try:
            result = search_changes.query_tb_temp()
            connect = pyodbc.connect("DSN=A2KSA")
            cursor = connect.cursor()
            cursor.execute("""SELECT
                                        FI_CODIGO,
                                        CASE WHEN A.FI_DESCRIPCION <> B.FI_DESCRIPCION THEN A.FI_DESCRIPCION
                                            ELSE '0' END AS DESCRIPCION,
                                        
                                        CASE WHEN A.FI_INTERNET <> B.FI_INTERNET THEN A.FI_INTERNET
                                            ELSE NULL END AS INTERNET,

                                        CASE WHEN A.PRECIO01 <> B.PRECIO01 THEN A.PRECIO01
                                            ELSE -1 END AS PRECIO01,

                                        CASE WHEN A.PRECIO02 <> B.PRECIO02 THEN A.PRECIO02
                                            ELSE -1 END AS PRECIO02,

                                        CASE WHEN A.PRECIO03 <> B.PRECIO03 THEN A.PRECIO03
                                            ELSE -1 END AS PRECIO03,

                                        CASE WHEN A.PRECIO04 <> B.PRECIO04 THEN A.PRECIO04
                                            ELSE -1 END AS PRECIO04
                                        
                                        FROM "C:/a2CA2020/Empre001/TMP/TABLA_A" A
                                        INNER JOIN "C:/a2CA2020/Empre001/TMP/TABLA_B" B ON A.FI_CODIGO = B.FI_CODIGO
                                        WHERE 
                                        A.FI_INTERNET <> B.FI_INTERNET OR 
                                        A.FI_DESCRIPCION <> B.FI_DESCRIPCION OR
                                        A.PRECIO01 <> B.PRECIO01 OR
                                        A.PRECIO02 <> B.PRECIO02 OR
                                        A.PRECIO03 <> B.PRECIO03 OR
                                        A.PRECIO04 <> B.PRECIO04

                            """)
            search = cursor.fetchall()
            if len(search) > 0:
                var_put = send_api_cloud.put(search)
                if var_put != '400':
                  UPDATE = True
                else:
                    sys.exit()  
            else:
                pass          
            update = search_changes.search_new_register()
            if update == list:
                var_post = send_api_cloud.post(update)
                if var_post != '400':
                    NEW_PRODUCTS = True
            else:      
                pass
            if NEW_PRODUCTS == True or UPDATE == True:
                search_changes.convert_tableA_toB()
                connect.close()
            else:
                connect.close()
                sys.exit()
           
        except Exception as e:
            print(e)
            return str(e)
        
ini = search_changes.search_update()   