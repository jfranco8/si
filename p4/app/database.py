# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # TODO: implementar la consulta; asignar nombre 'cc' al contador resultante
    orderdate = anio+mes

    if use_prepare:
        query = "PREPARE getListaCliMes(varchar, integer) as SELECT count(DISTINCT customerid) as cc FROM orders WHERE totalamount > $2 and TO_CHAR(orderdate, 'YYYYMM') = $1;"
        db_conn.execute(query)

    # TODO: ejecutar la consulta
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False

    # Array con resultados de la consulta para cada umbral
    dbr=[]

    for ii in range(niter):

        # TODO: ...

        if use_prepare:
            query = "EXECUTE getListaCliMes ('"+str(anio)+str(mes)+"', "+str(iumbral)+");"
            res = list(db_conn.execute(query))[0]
        else:
            query = "SELECT count(DISTINCT customerid) as cc FROM orders WHERE totalamount >" + str(iumbral)  +" and TO_CHAR(orderdate, 'YYYYMM') = '" + str(orderdate) + "'"
            res = list(db_conn.execute(query))[0]

        # Guardar resultado de la query
        dbr.append({"umbral":iumbral,"contador":res['cc']})

        if break0 == True and res['cc'] == 0:
            break

        # TODO: si break0 es True, salir si contador resultante es cero

        # Actualizacion de umbral
        iumbral = iumbral + iintervalo

    if use_prepare:
        query = "DEALLOCATE getListaCliMes"
        db_conn.execute(query)

    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)

    resultproxy.close()

    db_conn.close()

    return a

def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()

    db_conn.close()

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}

def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):

    # Array de trazas a mostrar en la página
    dbr=[]

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()

    #Eliminamos tablas de 1 en 1 para hacer commit intermedio y error integridad
    #Borramos contenido de orderdetail
    query1 = "DELETE * FROM orderdetail USING orders WHERE orderdetail.orderid = orders.orderid AND orders.customerid = '" + customerid + "'"

    #Borramos contenido de orders
    query2 = "DELETE * FROM orders WHERE customerid = '" + customerid + "'"

    #Borramos contenido de customers
    query3 = "DELETE * FROM customers WHERE customerid = '" + customerid + "'"

    #Transacción vía sentencias SQL
    if bSQL == True:
        db_conn = db_engine.connect()
        try:
            db_conn.execute("BEGIN")
            dbr.append('BEGIN ejecutado')
            db_conn.execute(query1)
            dbr.append('Pedidos de orderdetail borrados')

            #Ejecutar commit intermedio
            if bCommit == True:
                db_conn.execute("COMMIT")
                dbr.append('COMMIT intermedio ejecutado')
                db_conn.execute("BEGIN")
                dbr.append('BEGIN intermedio ejecutado')

            #Provocar error de integridad (eliminando el customer antes que sus orders)
            if bFallo == True:
                db_conn.execute(query3)
                dbr.append('Usuario customerid eliminado de customers')
                db_conn.execute(query2)
                dbr.append('Pedidos de orders borrados')

            #Sin error de integridad
            else:
                db_conn.execute(query2)
                dbr.append('Pedidos de orders borrados')
                db_conn.execute(query3)
                dbr.append('Usuario customerid eliminado de customers')

            query = "SELECT * FROM pg_sleep ('" + duerme + "');"
            db_conn.execute(query)
            dbr.append('Duerme ' + duerme + ' segundos')

            db_conn.execute("COMMIT")
            dbr.append('COMMIT final ejecutado')

        #Ejecutar ROLLBACK en caso de error
        except exc.IntegrityError:
            db_conn.execute("ROLLBACK")
            dbr.append('ROLLBACK ejecutado debido a un error')

    #Transacción vía funciones SQLAlchemy
    else:
        connection = engine.connect()
        db_conn = connection.begin()
        dbr.append('BEGIN ejecutado')
        try:
            db_conn.execute(query1)
            dbr.append('Pedidos de orderdetail borrados')

            #Ejecutar commit intermedio
            if bCommit == True:
                db_conn.commit()
                dbr.append('COMMIT intermedio ejecutado')
                db_conn = connection.begin()
                dbr.append('BEGIN intermedio ejecutado')

            #Provocar error de integridad (eliminando el customer antes que sus orders)
            if bFallo == True:
                connection.execute(query3)
                dbr.append('Usuario customerid eliminado de customers')
                connection.execute(query2)
                dbr.append('Pedidos de orders borrados')

            #Sin error de integridad
            else:
                connection.execute(query2)
                dbr.append('Pedidos de orders borrados')
                connection.execute(query3)
                dbr.append('Usuario customerid eliminado de customers')

            query = "SELECT * FROM pg_sleep ('" + duerme + "');"
            connection.execute(query)
            dbr.append('Duerme ' + duerme + ' segundos')

            db_conn.commit()
            dbr.append('COMMIT final ejecutado')
        except exc.IntegrityError:
            db_conn.rollback()
            dbr.append('ROLLBACK ejecutado debido a un error')

    db_conn.close()
    return dbr
