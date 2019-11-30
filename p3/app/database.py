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

def masVistas():
    query =  "select * from products natural join inventory natural join imdb_movies \
                order by sales desc limit 10"
    db_result = db_conn.execute(query)
    return list(db_result)

def topventas():
    db_result = db_conn.execute("SELECT * FROM getTopVentas('1990') LIMIT 15")
    return list(db_result)

def getmovie(id):
    db_result = db_conn.execute("SELECT * FROM imdb_movies WHERE movieid = " + id)
    return  list(db_result)

def getactors_movie(id):
    db_result = db_conn.execute("SELECT * FROM imdb_actormovies NATURAL JOIN imdb_actors WHERE movieid = " + id + " ORDER BY actorname")
    return  list(db_result)

def getdirectors_movie(id):
    db_result = db_conn.execute("SELECT * FROM imdb_directormovies NATURAL JOIN imdb_directors WHERE movieid = " + id + " ORDER BY directorname")
    return  list(db_result)

def getgenres_movie(id):
    db_result = db_conn.execute("SELECT * FROM movie_genre natural join genres WHERE movieid = " + id)
    return  list(db_result)

def getgenres():
    db_result = db_conn.execute("SELECT * FROM genres")
    return  list(db_result)

def getmoviesbygenre(genre):
    db_result = db_conn.execute("SELECT * FROM imdb_movies natural join genres WHERE genreid = " + str(genre))
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

def isuser(name):
    db_result = db_conn.execute("SELECT email FROM customers WHERE email = '" + name + "'")
    res = list(db_result)
    if res:
        return True
    return False

def getuser(name):
    db_result = db_conn.execute("SELECT * FROM customers WHERE email = '" + name + "'")
    return list(db_result)

def getPeliculasInCarrito(user_id):
    query = "select * from orders natural join orderdetail natural join products natural join imdb_movies where orderid = " + str(getCurrentOrder(user_id))
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
        current_order = createCurrentOrder(user)
    else:
        current_ord = db_list[0]
        current_order = str(current_ord)[1:-2]
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
    query = "select count(*) from orderdetail where orderid = "+str(order_id)+" and prod_id = "+str(prod_id)
    num_peliculas = int(str(list(db_conn.execute(query))[0])[1:-2])
    if num_peliculas == 0:
        query = "insert into orderdetail(orderid, prod_id, price, quantity) values (" +str(order_id)+ ", " +str(prod_id)+ ", " +str(price)+ ", 1)"
    else:
        query = "select quantity from orderdetail where orderid = "+str(order_id)+" and prod_id = "+str(prod_id)
        quantity = int(str(list(db_conn.execute(query))[0])[1:-2]) + 1
        query = "update orderdetail set quantity = "+ str(quantity)+ " where orderid = "+str(order_id)+" and prod_id = "+str(prod_id)
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
    query = "select quantity from orderdetail where orderid = "+str(order_id)+" and prod_id = "+str(prod_id)
    quantity = int(str(list(db_conn.execute(query))[0])[1:-2])
    if quantity == 1:
        query = "delete from orderdetail where (orderid = " + str(order_id) + " and prod_id = " + str(prod_id) + ")"
    else:
        quantity = quantity - 1
        quantity = str(quantity)
        query = "update orderdetail set quantity = "+ str(quantity)+ " where orderid = "+str(order_id)+" and prod_id = "+str(prod_id)
    db_conn.execute(query)

def buscarPeli(busqueda):
    query = "select * from imdb_movies where lower(movietitle) like '%%" + str(busqueda) + "%%'"
    db_result = db_conn.execute(query)
    return list(db_result)

def setpsw(id_usuario, new_psw_encode):
    query = "UPDATE customers SET password = '" + str(new_psw_encode) + "' WHERE customerid = " + str(id_usuario)
    db_result = db_conn.execute(query)

def getPeliculasOrder(orderid):
    query = "select movieid, price, quantity, movietitle, orderdate, cast(totalamount as decimal(10,2)) from orderdetail natural join products natural join imdb_movies natural join orders where orderid = " + str(orderid)
    db_result = db_conn.execute(query)
    dict = [{'movieid': col1,
            'price': col2,
            'quantity': col3,
            'movietitle': col4,
            'orderdate': col5,
            'totalamount': col6}
            for (col1, col2, col3, col4, col5, col6) in db_result
            ]
    return dict

def getPaidOrders(user_id):
    query = "select orderid from orders where customerid = " + str(user_id) + " and status = 'Paid'"
    db_result = db_conn.execute(query)
    return list(db_result)

def getHistorial(user_id):
    orders = getPaidOrders(user_id)
    pedidos = []
    for ord in orders:
        new_order = str(ord)[1:-2]
        pelis = getPeliculasOrder(new_order)
        pelis_dict = {'pedidos': pelis}
        pedidos.append(pelis_dict)
    return pedidos
