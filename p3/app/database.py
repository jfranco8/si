# -*- coding: utf-8 -*-

import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# conexion a la base de datos
db_conn = None
db_conn = db_engine.connect()

def todas():
    db_result = db_conn.execute("SELECT * FROM imdb_movies ORDER BY movietitle")
    return  list(db_result)

def novedades():
    db_result = db_conn.execute("SELECT * FROM imdb_movies ORDER BY year DESC LIMIT 20")
    return  list(db_result)

def topventas():
    db_result = db_conn.execute("SELECT * FROM getTopVentas('1990') LIMIT 15")
    return list(db_result)

def getmovie(id):
    db_result = db_conn.execute("SELECT * FROM imdb_movies WHERE movieid = " + id)
    return  list(db_result)

def getactors(id):
    db_result = db_conn.execute("SELECT * FROM imdb_actormovies NATURAL JOIN imdb_actors WHERE movieid = " + id + " ORDER BY actorname")
    return  list(db_result)

def getdirectors(id):
    db_result = db_conn.execute("SELECT * FROM imdb_directormovies NATURAL JOIN imdb_directors WHERE movieid = " + id + " ORDER BY directorname")
    return  list(db_result)

def getgenres(id):
    db_result = db_conn.execute("SELECT * FROM movie_genre natural join genres WHERE movieid = " + id)
    return  list(db_result)

def getproduct(id):
    db_result = db_conn.execute("SELECT * FROM products WHERE movieid = " + id)
    return list(db_result)

def getMaxIdCustomer():
    db_result = db_conn.execute("SELECT MAX(customerid) FROM customers")
    return list(db_result)

def getNumberUsersWithUsername(username):
    db_result = db_conn.execute("SELECT count(customerid) FROM customers WHERE username = '" + username + "'")
    return list(db_result)

def adduser(id_cust, user, password_cif, nombre, mail, tarjeta, cvc, saldo):
    new_nombre = str(nombre)
    new_nombre = new_nombre[1:-2]
    new_mail = str(mail)
    new_mail = new_mail[1:-2]
    new_tarj = str(tarjeta)
    new_tarj = new_tarj[1:-2]
    new_cvc = str(cvc)
    new_cvc = new_cvc[1:-2]
    query = "INSERT INTO customers (customerid,firstname,lastname,address1,city,country,email,creditcardtype,creditcard,creditcardexpiration,username,password,cvc,income,region)"
    query += " VALUES ("
    query += str(id_cust)
    query += ","
    query += new_nombre
    query += ",' ','EPS UAM','Madrid','Spain',"
    query += new_mail
    query += ",'Mastercard',"
    query += new_tarj
    query += ",'202203','"
    query += user
    query += "','"
    query += str(password_cif)
    query += "',"
    query += new_cvc
    query += ","
    query += str(saldo)
    query += ", ' ')"
    db_conn.execute(query)

    # db_conn.execute("INSERT INTO customers (firstname,lastname,address1,city,country,email,creditcardtype,creditcard,creditcardexpiration,username,password,cvc,money) VALUES ("+nombre+",' ','EPS UAM','Madrid','Spain',"+mail",'Mastercard',"+tarjeta+",'202203',"+user+","+password_cif+","+cvc+","+saldo+")")
def isuser(name):
    db_result = db_conn.execute("SELECT email FROM customers WHERE email = '" + name + "'")
    res = list(db_result)
    if res:
        return True
    return False

def getuser(name):
    db_result = db_conn.execute("SELECT * FROM customers WHERE email = '" + name + "'")
    return list(db_result)

def inserIntoCarrito(customerid, productoid):
    db_conn.execute("INSERT INTO carrito(customerid, prod_id) VALUES ( " + customerid +  ", " + productoid + " )")

def getPeliculasInCarrito(user_id):
    query = "select * from orders natural join orderdetail natural join products natural join imdb_movies where orderid = " + str(getCurrentOrder(user_id))
    # query = "select * from (	select movietitle, price, prod_id, movieid 	from (select * from carrito natural join products where carrito.prod_id = products.prod_id) as T4 natural join imdb_movies where T4.movieid = imdb_movies.movieid) as T"
    db_result = db_conn.execute(query)
    return list(db_result)

def getPeliculasProdById(movieid):
    query = "select * from (	select *  from products  natural join imdb_movies where products.movieid = imdb_movies.movieid) as T where T.movieid = " + str(movieid)
    db_result = db_conn.execute(query)
    return list(db_result)

def getUserSaldo(email):
    query = "select income from customers where email = '"+ str(email) +"'"
    db_result = db_conn.execute(query)
    return list(db_result)

# user es el userId
def getCurrentOrder(user):
    query = "select orderid from orders where customerid = " + str(user) + " and status = ''"
    db_result = db_conn.execute(query)
    db_list = list(db_result)
    if db_list == []:
        print('0NO HABIA Y CREA UN')
        current_order = createCurrentOrder(user)
    else:
        print('Hay u order abierto que es:')
        current_ord = db_list[0]
        current_order = str(current_ord)[1:-2]
        print(current_order)
    return current_order

def getMaxOrderId():
    query = "select max(orderid) from orders"
    db_result = db_conn.execute(query)
    return list(db_result)[0]

def createCurrentOrder(user):
    new_order_id = int(str(getMaxOrderId())[1:-2]) + 1
    order_id = str(new_order_id)
    query = "insert into orders (orderid, customerid, orderdate, netamount, tax, totalamount, status) values ("+order_id+", "+str(user)+", now(), 0, 0, 0, '')"
    db_conn.execute(query)
    return new_order_id

def insertIntoOrders(price, user_id, prod_id):
    order_id = str(getCurrentOrder(user_id))
    query = "insert into orderdetail(orderid, prod_id, price, quantity) values (" +str(order_id)+ ", " +str(prod_id)+ ", " +str(price)+ ", 1)"
    db_conn.execute(query)

def setUserSaldo(customerid, saldo):
    query = "update customers set income = " + str(saldo) + " where customerid = " +str(customerid)
    db_conn.execute(query)

def setOrderStatusPaid(user):
    query = "update orders set status = 'Paid' where customerid = " + str(user)
    db_conn.execute(query)

def getOrderPrice(user):
    order_id = str(getCurrentOrder(user))
    query = "select totalamount from orders where orderid = " + order_id
    db_result = db_conn.execute(query)
    return list(db_result)

def borrarProductoCarrito(prod_id, user_id):
    order_id = str(getCurrentOrder(user_id))
    query = "delete from orderdetail where orderid = " + str(order_id) + " and prod_id = " + str(prod_id)
    db_conn.execute(query)
