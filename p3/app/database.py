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

# esta funcion devuelve la tabla como tal, no se si vale para leerla luego en el routes.py
def novedades():
    # Seleccionar las peliculas del este anno
    db_result = db_conn.execute("SELECT * FROM imdb_movies ORDER BY year DESC LIMIT 20")
    return  list(db_result)
