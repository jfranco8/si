#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, Flask, make_response
import json
import os
import sys
from hashlib import md5
import random
from os.path import isdir
import time
from app import database

@app.route('/')
@app.route('/index')
def index():
    print(url_for('static', filename='styles.css'))
    movies = database.todas()
    genres = database.getgenres()
    titulo = "Todas las muuuvies"
    return render_template('index.html', title = titulo, movies = movies, genres = genres)

#tipos de pelis
@app.route('/novedades')
def novedades():
    print(url_for('static', filename='styles.css'))
    movies = database.novedades()
    genres = database.getgenres()
    titulo = "Novedades"
    return render_template('index.html', title = titulo, movies = movies, genres = genres)


@app.route('/masvistas')
def masvistas():
    print(url_for('static', filename='styles.css'))
    movies = database.masVistas()
    titulo = "Muuuvies mas vistas"
    genres = database.getgenres()
    return render_template('index.html', title = titulo, movies = movies, genres = genres)


@app.route('/topventas')
def ventas():
    print(url_for('static', filename='styles.css'))
    movies = database.topventas()
    genres = database.getgenres()
    titulo = "Top ventas por año"
    return render_template('index.html', title = titulo, movies = movies, genres = genres)

#categorias de pelis
@app.route('/categorias/<cat>')
def categorias(cat):
    print(url_for('static', filename='styles.css'))
    genres = database.getgenres()
    titulo = genres[int(cat)-1]['genre']
    genreid = genres[int(cat)-1]['genreid']
    print("QUEREMOS EL GENRE DE ID", genreid)
    pelis = database.getmoviesbygenre(genreid)
    return render_template('index.html', title = titulo, movies = pelis, genres = genres)

#peli concreta
@app.route('/pelicula/<valor>/', methods=['GET', 'POST'])
def pelicula(valor):
    print(url_for('static', filename='styles.css'))
    genres = database.getgenres()
    peli = database.getmovie(valor)[0]
    categorias = database.getgenres_movie(valor)
    actores = database.getactors_movie(valor)
    directores = database.getdirectors_movie(valor)
    producto = database.getproduct(valor)[0]

    if 'usuario' not in session:
        if request.method == 'POST':
            if not 'carrito' in session:
                session['carrito'] = []
            session['carrito'].append(producto)

    else:
        if request.method == 'POST':
            user = session['usuario']
            usuarios = database.getuser(user)
            id_usuario=usuarios[0]['customerid']
            # INSERT A ORDERDETAIL PARA ORDER CON STATUS NULL
            # database.getCurrentOrder()
            # database.inserIntoCarrito(str(id_usuario), str(producto['prod_id']))
            database.insertIntoOrders(producto['price'], str(id_usuario), producto['prod_id'])

    return render_template('pelicula.html', peli = peli, genres = genres, categorias = categorias, directores = directores, actores = actores, producto = producto)

#busqueda de peli
@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    print(url_for('static', filename='styles.css'))
    genres = database.getgenres()
    if 'busqueda' in request.form:
        buscado = request.form['busqueda']
        buscado = str(buscado).lower()
        pelis = database.buscarPeli(buscado)
        return render_template('index.html', title = buscado, genres = genres, movies=pelis)
    else:
        return redirect(url_for('index'))


@app.route('/ayuda')
def ayuda():
    genres = database.getgenres()
    return render_template('ayuda.html', genres = genres)


@app.route('/cambiar_contrasena/<usuario>/', methods=['GET', 'POST'])
def cambiar_contrasena(usuario):
    genres = database.getgenres()
    user = session['usuario']
    usuarios = database.getuser(user)
    usuario = usuarios[0]
    passw = usuario['password'] #ps
    id_usuario = usuario['customerid']

    if request.method == 'POST':
        old_contr = request.form['old']
        new_contr1 = request.form['new1']
        new_contr2 = request.form['new2']

        if md5(old_contr.encode()).hexdigest() != passw:
            return render_template('cambiar_contrasena.html', title = "Cambiar contrasena", mal=True, distintas=False, genres = genres)

        if new_contr1 == new_contr2:
            # # Código para guardar las contraseñas cifradas
            # # Lo comentamos porque en la base de datos proporcionada no están cifradas
            # new_psw_encode = md5(new_contr1.encode()).hexdigest()
            # database.setpsw(id_usuario, new_psw_encode)
            database.setpsw(id_usuario, new_contr1)

            return redirect(url_for('index'))
        else:
            return render_template('cambiar_contrasena.html', title = "Cambiar contrasena", mal=False, distintas=True, genres = genres)
    return render_template('cambiar_contrasena.html', title = "Cambiar contrasena", mal=False, distintas=False, genres = genres)


@app.route('/perfil/', methods=['GET', 'POST'])
def perfil():
    genres = database.getgenres()
    user = session['usuario']
    usuarios = database.getuser(user)
    usuario = usuarios[0]
    id_usuario = usuario['customerid']
    username = usuario['username'] #nombre de usuario
    passw = usuario['password'] #ps
    name = usuario['firstname'] #nombre
    mail = usuario['email'] #mail
    card = usuario['creditcard'] #tarjeta
    cvc = usuario['cvc'] #cvc
    saldo = usuario['income'] #saldo
    error = False

    if request.method == 'POST':
        saldo_new = request.form['saldo_nuevo']
        if float(saldo_new) < 0:
            error = True
        else:
            saldo = float(saldo) + float(saldo_new)
            database.setUserSaldo(id_usuario,saldo)

    return render_template('perfil.html', genres = genres, name=name, passw=passw, username=username, mail=mail, card=card, saldo=saldo, error=error, title=username)


@app.route('/historial',methods=['GET', 'POST'])
def historial():
    user = database.getuser(session['usuario'])
    userid = str(user[0]['customerid'])
    print("queremos los pedidos hechos por", userid)
    historial = database.getHistorial(str(userid))
    genres = database.getgenres()
    # path = os.path.dirname(__file__)
    # path += "/usuarios/"+session['usuario']
    # historial = json.load(open(path+"/historial.json"))['pedidos']
    # datos = json.load(open(path+"/datos.json"))
    # historial.reverse()
    datos = user[0]
    return render_template('historial.html', genres = genres, title = "Historial", pedidos=historial, datos=datos)
    return redirect(url_for('index'))


@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    genres = database.getgenres()
    no_saldo = False
    no_registrado = False
    compra = False

    if not 'carrito' in session:
        session['carrito'] = []


    if request.method == 'POST':

        if 'usuario' in session:

            user = session['usuario']
            usuarios = database.getuser(user)

            # path = os.path.dirname(__file__)
            # path += "/usuarios/"+session['usuario']+"/"
            # datos = json.load(open(path+"datos.json"))
            # saldo=datos['saldo']
            saldo = database.getUserSaldo(session['usuario'])
            saldo = str(saldo)[2:-3]
            coste = database.getOrderPrice(usuarios[0]['customerid'])
            coste = str(coste)[11:-5]

            if float(coste) <= float(saldo):
                saldo = float(saldo) - float(coste)
                # setOrderStatus(Paid)
                # Decrementar la cantidad del usuario
                database.setOrderStatusPaid(str(usuarios[0]['customerid']))
                database.setUserSaldo(str(usuarios[0]['customerid']), saldo)
                compra = True

            else:
                no_saldo = True


                # iculas_nombre = database.getPeliculasInCarrito()
                # no_registrado = True
                # print("AQUIIIII", peliculas_nombre)
                # return render_template('carrito.html', title = "Carrito", peliculas=peliculas_nombre,compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)
            all_carrito = database.getPeliculasInCarrito(str(usuarios[0]['customerid']))
            return render_template('carrito.html', genres = genres, title = "Carrito", peliculas=all_carrito,compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)


        else:
            # No registrado
            peliculas_nombre = []
            for prod in session['carrito']:
                peliculas_nombre.append(database.getPeliculasProdById(prod['movieid'])[0])
            no_registrado = True
            return render_template('carrito.html', genres = genres, title = "Carrito", peliculas=peliculas_nombre,compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)

    else:

        if 'usuario' in session:

            user = session['usuario']
            usuarios = database.getuser(user)

            if session['carrito'] != []:
                for prod in session['carrito']:
                    pelicula = database.getPeliculasProdById(prod['movieid'])[0]
                    database.insertIntoOrders( str(pelicula['price']), str(usuarios[0]['customerid']), str(pelicula['prod_id']))
                session['carrito'] = []
            all_carrito = database.getPeliculasInCarrito(str(usuarios[0]['customerid']))
            return render_template('carrito.html', genres = genres, title = "Carrito", peliculas=all_carrito,compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)

        else:
            peliculas_nombre = []
            for prod in session['carrito']:
                peliculas_nombre.append(database.getPeliculasProdById(prod['movieid'])[0])
            return render_template('carrito.html', genres = genres, title = "Carrito", peliculas=peliculas_nombre,compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)


    return render_template('carrito.html', genres = genres, title = "Carrito", peliculas=session['carrito'],compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)


@app.route('/carrito/borrar/<valor>')
def carrito_borrar(valor):
    if 'usuario' in session:

        user = session['usuario']
        usuarios = database.getuser(user)
        id_usuario=usuarios[0]['customerid']

        database.borrarProductoCarrito(valor, id_usuario)

        return redirect(url_for('carrito'))

    else:
        for p in session['carrito']:
            if p['prod_id'] == int(valor):
                session['carrito'].remove(p)
                break

        return redirect(url_for('carrito'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    genres = database.getgenres()
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        if request.method == 'POST':
            user = request.form['username']
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('userID', request.form['username'])

        if not database.isuser(user):
            return render_template('login_registro.html', genres = genres, title = "Log In", existe=True)
        else:
            usuarios = database.getuser(user)
            mail_usuario=usuarios[0]['email']
            passw_cif=usuarios[0]['password']
            # passw = md5(request.form['password'].encode()).hexdigest()
            passw = request.form['password']
            # aqui se deberia validar con fichero .dat del usuario
            cond = request.form['username'] == mail_usuario and passw_cif == passw
            if cond:
                session['usuario'] = request.form['username']
                session.modified = True
                if not 'carrito' in session:
                    session['carrito'] = []
                # se puede usar request.referrer para volver a la pagina desde la que se hizo login

                return resp
            else:
                # aqui se le puede pasar como argumento un mensaje de login invalido

                return render_template('login_registro.html', genres = genres, title = "Log In", existe=False)
    else:
        # se puede guardar la pagina desde la que se invoca
        session['url_origen']=request.referrer
        session.modified=True
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        return render_template('login_registro.html', genres = genres, title = "Log In", existe=False)

@app.route('/registro', methods=['GET', 'POST'])
def signup():
    genres = database.getgenres()
    if 'username' in request.form:
        if request.form['password']  == request.form['password2']:

            if request.method == 'POST':
                user = request.form['username']
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('userID', request.form['mail'])

                # password_cif = md5(request.form['password'].encode()).hexdigest()
                password_cif = request.form['password']
                nombre = request.form['nombre'],
                mail = request.form['mail'],
                tarjeta = request.form['tarjeta'],
                cvc = request.form['cvc'],
                saldo = random.randrange(100)
                id_cust_n = str(database.getMaxIdCustomer()[0])
                id_cust_n = id_cust_n[1:-2]
                id_cust = int(id_cust_n) + 1

                num_user_username = str(database.getNumberUsersWithUsername(user)[0])
                num_user_username = num_user_username[1:-2]
                num_user_username = int(num_user_username)
                if num_user_username != 0:
                    return render_template('registro.html', genres = genres, title = "Sign", existe=True)

                database.adduser(id_cust, user, password_cif, nombre, mail, tarjeta, cvc, saldo);

                session['usuario'] = request.form['mail']
                session.modified = True

                # historial.close()
                return resp
            else:
                return render_template('registro.html', genres = genres, title = "Sign", existe=True)
        else:
            return render_template('registro.html', genres = genres, title = "Sign", existe=False)
    return render_template('registro.html', title = "Sign", genres = genres, existe=False)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    session['carrito'] = []
    # session.pop('carrito', None)
    return redirect(url_for('index'))
