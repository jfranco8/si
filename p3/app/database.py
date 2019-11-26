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
    db_result = db_conn.execute("SELECT * FROM imdb_moviegenres WHERE movieid = " + id)
    return  list(db_result)

def getproduct(id):
    db_result = db_conn.execute("SELECT * FROM products WHERE movieid = " + id)
    return list(db_result)

def adduser(user, password_cif, nombre, mail, tarjeta, cvc, saldo):
    db_conn.execute("INSERT INTO customers (firstname,lastname,address1,city,country,email,creditcardtype,creditcard,creditcardexpiration,username,password,cvc,money) VALUES ("+nombre+",' ','EPS UAM','Madrid','Spain',"+mail",'Mastercard',"+tarjeta+",'202203',"+user+","+password_cif+","+cvc+","+saldo+")")
