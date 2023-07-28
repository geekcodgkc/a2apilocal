import json
import glob
import sys
import os
import pyodbc
from datetime import datetime
class search_socket_data():
    def function_order(nro_order):
        str_nro_order = str(nro_order)
        if len(str_nro_order) <= 8:
            str_nro_order = "WEB".ljust( 11 - len(str_nro_order), "0") + str_nro_order
            return str_nro_order
        
    def function_id(rif: str):
            if len(rif) == 12:
                id = rif[2:10]
            if len(rif)==13:
                id=rif[2:11]
            if len(rif) < 10:
                id = rif[1:9]        
            return id

    def search_orders():
        orders_list = glob.glob("C:/ApiRestFlask/64c288f21c6ae38263de2cbf.json")
        if len(orders_list) > 0:
            path_order = orders_list[0]
            if os.stat(path_order).st_size > 0:
                cant_items = 0
                index = 0
                total_8, total_16 = 0, 0

                with open(path_order, mode='r') as file:
                    order = json.load(file)
                    products = order['products']
            nro_order=search_socket_data.function_order(order['orderNumber'])           
            for i in products:    
                cant_items = cant_items + i['qty']
                if i['product']['tax'] == 8:
                    index8 = (i['price'] -1)
                    lists = list(i['product']['prices'].values())
                    total_8 =  total_8 + lists[index8] * i['qty']
                if i['product']['tax'] == 16:
                    index16= (i['price'] -1)
                    lists16 = list(i['product']['prices'].values())
                    total_16 = total_16 + lists16[index16] * i['qty']  
            print(total_16)
            print(total_8)                    

            print(cant_items)        
            connect= pyodbc.connect("DSN=A2KSA")
            cur = connect.cursor()
            try:
                id_client = search_socket_data.function_id(order['client']['rif'])
                cur.execute(f"""INSERT INTO SOPERACIONINV
                                (FTI_DOCUMENTO, FTI_VISIBLE, FTI_MONEDA, FTI_TIPO, FTI_RESPONSABLE, FTI_PERSONACONTACTO, FTI_DOCUMENTOORIGEN, FTI_STATUS, FTI_FECHAEMISION,
                                FTI_DEPOSITOSOURCE, FTI_TOTALITEMS, FTI_TOTALBRUTO, FTI_BASEIMPONIBLE, FTI_IMPUESTO1PORCENT, FTI_IMPUESTO1MONTO, FTI_TOTALNETO, FTI_FACTORCAMBIO,
                                FTI_TOTALCOSTO, FTI_TOTALCOSTOREAL, FTI_CLASIFICACION, FTI_DESCRIPCLASIFY, FTI_USER, FTI_AUTORIZADOPOR, FTI_TIENELOTES, FTI_UPDATEITEMS, FTI_DESCUENTO1PORCENT,
                                FTI_DESCUENTO1MONTO, FTI_DESCUENTO2PORCENT, FTI_DESCUENTO2MONTO, FTI_DESCUENTOPARCIAL, FTI_FLETEPORCENT, FTI_FLETEMONEDA, FTI_RIFCLIENTE, FTI_SALDOOPERACION,
                                FTI_MONEDAPAGO, FTI_TOTALPRECIO, FTI_VUELTO, FTI_EXCENTO, FTI_COSTODEVENTA, FTI_TIPOOPERACIONORIGEN, FTI_VENDEDORASIGNADO, FTI_HORA, FTI_FACTORREFERENCIA, FTI_FECHALIBRO,
                            FTI_BASEIMPONIBLE2, FTI_IMPUESTO2PORCENT, FTI_IMPUESTO2MONTO)  
                        
                            VALUES('{nro_order}', 1, 2, 10, '{id_client}', '{order['client']['name']}', '{order['_id']}', 4, '{str(datetime.date(datetime.now()))}',
                            1, {cant_items}, {order['orderTotal']}, {total_16 / 1.16}, 16, {abs((total_16 / 1.16) - total_16)}, {order['orderTotal']}, 1,
                            0, 0, 0, '<Ninguna>', 1, 'Crédito', 0, 1, 0,
                            0, 0 , 0, 0, 0, 0, '{id_client}', {order['orderTotal']}, 1, {order['orderBase']}, 0, 0, 0, 0, '01', '{datetime.now().strftime("%H:%M:%S")}', 1,
                            '{str(datetime.date(datetime.now()))}', {total_8 / 1.08}, 8,{abs((total_8 / 1.08 ) - total_8)} )                         
                            
                            """)
                cur.commit()
                cur.execute(f"""SELECT LASTAUTOINC('SOPERACIONINV') FROM SOPERACIONINV WHERE FTI_DOCUMENTO = '{nro_order}' AND FTI_TIPO = 10 
                            TOP 1""")
                last_auto=cur.fetchone()
            except Exception as e:
                print(e)
                cur.rollback  
            try:
                linea = 0
                for i in products:
                    if i['price'] ==1:
                        price_unity = i['product']['prices']['p1']
                    if i['price']==2:
                        price_unity = i['product']['prices']['p2']
                    if i['price']==3:
                        price_unity = i['product']['prices']['p3']
                    if i['price']==4:
                        price_unity = i['product']['prices']['p4']

                    if i['product']['tax'] == 16:
                        tax_items = abs((price_unity / 1.16) - price_unity)
                        tax_items2 = 0
                        tax16 = 1 
                        tax8 = 0
                        base_items = price_unity / 1.16
                    if i['product']['tax'] == 8:
                        tax8= 1
                        tax16 = 0
                        tax_items = 0
                        tax_items2 = abs((price_unity / 1.08) - price_unity)
                        base_items = price_unity / 1.08
                    if i['product']['tax'] ==0:
                        tax_items = 0 / price_unity 
                        tax_items2 = 0 / price_unity
                        tax16 = 0
                        tax8 = 0   
                        base_items = price_unity    
                                          
                    cur.execute(f"""INSERT INTO SDETALLEVENTA
                                (FDI_CODIGO, FDI_OPERACION_AUTOINCREMENT, FDI_DOCUMENTO, FDI_TIPOOPERACION, FDI_LINEA, FDI_CLIENTEPROVEEDOR, FDI_DOCUMENTOORIGEN,
                                FDI_STATUS, FDI_VISIBLE, FDI_CANTIDAD, FDI_CANTIDADPENDIENTE, FDI_DEPOSITOSOURCE, FDI_DECIMALES, FDI_DECIMALESPEN, FDI_USASERIALES, 
                                FDI_USADEPOSITOS, FDI_MONEDA, FDI_FACTORCAMBIO,
                                FDI_IMPUESTO1, FDI_PORCENTIMPUESTO1, FDI_MONTOIMPUESTO1, FDI_IMPUESTO2, FDI_PORCENTIMPUESTO2, FDI_MONTOIMPUESTO2, FDI_PORCENTDESCPARCIAL, 
                                FDI_DESCUENTOPARCIAL, FDI_PRECIOSINDESCUENTO,
                                FDI_PRECIOCONDESCUENTO, FDI_PRECIODEVENTA, FDI_ROUNDDESCTPARCIAL, FDI_UNDDESCARGA, FDI_UNDCAPACIDAD, FDI_UNDDETALLADA, FDI_INDEXPRICES, 
                                FDI_VENDEDORASIGNADO,
                                FDI_MONTOCOMISION, FDI_PRECIOBASECOMISION, FDI_COMISIONBLOQUEADA, FDI_COMISIONYAPAGADA, FDI_FECHAOPERACION, FDI_USER, FDI_PORCENTDESCUENTO1, 
                                FDI_PORCENTDESCUENTO2)
                                
                                VALUES('{i['product']['id']}', {last_auto[0]}, '{nro_order}', 10, {str(linea)}, '{id_client}', '{order['_id']}', 
                                        4, 1, {str(i['qty'])}, {str(i['qty'])}, 1, 0, 0, 0, 1, 1, 1,
                                         16, {tax16}, {tax_items}, 8, {tax8}, {tax_items2}, 0, 0, {base_items}, {base_items}, {price_unity}, 0, 1, 1, 0, 0, '01', 0, {base_items}, 
                                         0, 0, '{str(datetime.date(datetime.now()))}', 1, 0, 0)""")
                
                    cur.commit()
                    linea += 1
            except Exception as e:
                print(e)    
            

ini = search_socket_data.search_orders()                