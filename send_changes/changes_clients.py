import os
import sys
import pyodbc

class changes_customer():

    def compare_GKCtableA_B():
        try:
            connect = pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            cur.execute("""SELECT FC_CODIGO, FC_GKC_INTERNET
                                INTO "C:/a2CA2020/Empre001/TMP/GKC_TABLEA"
                                FROM SCLIENTES
                            WHERE FC_STATUS = 1 """)
            cur.execute("""CREATE INDEX IF NOT EXISTS "FC_CODE" ON "C:/a2CA2020/Empre001/TMP/GKC_TABLEA" ("FC_CODIGO") """)

            cur.execute("""SELECT FC_CODIGO, FC_GKC_INTERNET
                            FROM "C:/a2CA2020/Empre001/TMP/GKC_TABLEA" A
                            INNER JOIN "C:/a2CA2020/Empre001/TMP/GKC_TABLEB" B ON A.FC_CODIGO = B.FC_CODIGO
                            WHERE A.FC_GKC_INTERNET <> B.FC_GKC_INTERNET """)
            actualiza = cur.fetchall()
            if actualiza > 0:
                return actualiza
            else:
                return False
        except Exception as e:
            return 'Error'    