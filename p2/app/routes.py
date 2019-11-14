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

# f = []
#
# def files(path):
#     for file in os.listdir(path):
#         os.path.join(path, file)
#         yield file
#
# for file in files("."):
#     f.append(file)

@app.route('/')
@app.route('/index')
def index():
    print(url_for('static', filename='styles.css'))
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Todas las muuuvies", movies=catalogue['peliculas'])

#tipos de pelis

@app.route('/novedades')
def novedades():
    print(url_for('static', filename='styles.css'))
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    pelis = []
    for p in catalogue['peliculas']:
        if p['novedades'] == True:
            pelis.append(p)
    titulo = "Novedades"
    return render_template('index.html', title = titulo, movies=pelis)


@app.route('/masvistas')
def masvistas():
    print(url_for('static', filename='styles.css'))
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    pelis = []
    titulo="Muuuvies mas vistas"
    for p in catalogue['peliculas']:
        if p['mas_vistas'] == True:
            pelis.append(p)
    return render_template('index.html', title = titulo, movies=pelis)

#categorias de pelis
@app.route('/categorias/<cat>')
def categorias(cat):
    print(url_for('static', filename='styles.css'))
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    pelis = []
    if cat=="animacion":
        titulo="Animación"
    elif cat=="aventura":
        titulo="Aventura"
    elif cat=="comedia":
        titulo="Comedia"
    elif cat=="drama":
        titulo="Drama"
    elif cat=="miedo":
        titulo="Miedo"
    elif cat=="musical":
        titulo="Musical"
    elif cat=="romantica":
        titulo="Romántica"
    else:
        titulo="Ciencia ficcion"
    for p in catalogue['peliculas']:
        for c in p['categorias']:
            if c['cat'] == titulo:
                pelis.append(p)
    return render_template('index.html', title = titulo, movies=pelis)

#peli concreta
@app.route('/pelicula/<valor>/', methods=['GET', 'POST'])
def pelicula(valor):
    print(url_for('static', filename='styles.css'))
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    for p in catalogue['peliculas']:
        if p['id'] == int(valor):
            if request.method == 'POST':
                if not 'carrito' in session:
                    session['carrito'] = []
                session['carrito'].append(p)
            return render_template('pelicula.html', title = p['titulo'], pelicula=p)
    return redirect(url_for('index'))

#busqueda de peli
@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    print(url_for('static', filename='styles.css'))
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    pelis = []
    if 'busqueda' in request.form:
        for p in catalogue['peliculas']:
            if request.form['busqueda'].lower() in p['titulo'].lower():
                pelis.append(p)
        return render_template('index.html', title = request.form['busqueda'], movies=pelis)
    else:
        return redirect(url_for('index'))


@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')


@app.route('/cambiar_contrasena/<usuario>/', methods=['GET', 'POST'])
def cambiar_contrasena(usuario):
    path = os.path.dirname(__file__)
    path += "/usuarios/"+usuario+"/"
    datos = json.load(open(path+"datos.json"))
    passw=datos['psw']

    if request.method == 'POST':
        old_contr = request.form['old']
        new_contr1 = request.form['new1']
        new_contr2 = request.form['new2']

        if md5(old_contr.encode()).hexdigest() != passw:
            return render_template('cambiar_contrasena.html', title = "Cambiar contrasena", mal=True)

        datos = json.load(open(path+"datos.json"))
        datos['psw'] = md5(new_contr1.encode()).hexdigest()

        with open(path+"datos.json", 'w') as f:
            f.write(json.dumps(datos))

        return redirect(url_for('index'))
    return render_template('cambiar_contrasena.html', title = "Cambiar contrasena", mal=False)


@app.route('/perfil/<usuario>/', methods=['GET', 'POST'])
def perfil(usuario):
    path = os.path.dirname(__file__)
    path += "/usuarios/"+usuario+"/"
    datos = json.load(open(path+"datos.json"))
    username=datos['username'] #nombre de usuario
    passw=datos['psw'] #ps
    name=datos['nombre'] #nombre
    mail=datos['mail'] #mail
    card=datos['tarjeta'] #tarjeta
    cvc=datos['cvc'] #cvc
    saldo=datos['saldo'] #saldo
    error = False

    if request.method == 'POST':
        saldo_new = request.form['saldo_nuevo']
        if float(saldo_new) < 0:
            error = True
        else:
            saldo = float(saldo) + float(saldo_new)
        datos = json.load(open(path+"datos.json"))
        datos['saldo']=saldo
        with open(path+"datos.json", 'w') as f:
            f.write(json.dumps(datos))
    return render_template('perfil.html', name=name, passw=passw, username=username,
        mail=mail, card=card, saldo=saldo, error=error)


@app.route('/historial',methods=['GET', 'POST'])
def historial():
    path = os.path.dirname(__file__)
    path += "/usuarios/"+session['usuario']
    historial = json.load(open(path+"/historial.json"))['pedidos']
    datos = json.load(open(path+"/datos.json"))
    historial.reverse()
    return render_template('historial.html', title = "Historial", pedidos=historial, datos=datos)


@app.route('/carrito', methods=['GET', 'POST'])
def carrito():

    no_saldo = False
    no_registrado = False
    compra = False

    if not 'carrito' in session:
        session['carrito'] = []


    if request.method == 'POST':

        if session['carrito'] != []:

            if 'usuario' in session:

                path = os.path.dirname(__file__)
                path += "/usuarios/"+session['usuario']+"/"
                datos = json.load(open(path+"datos.json"))
                saldo=datos['saldo']

                coste = 0

                for p in session['carrito']:
                    coste += float(p['precio'])

                if float(coste) <= float(saldo):
                    saldo -= coste

                    data = json.load(open(path+'historial.json'))
                    pedido = {
                        'fecha' : time.strftime("%d.%m.%Y"),
                        'total' : coste,
                        'peliculas' : []
                    }
                    for p in session['carrito']:
                        pedido['peliculas'].append(p)
                    data['pedidos'].append(pedido)

                    with open(path+'historial.json', 'w') as file:
                        json.dump(data, file)

                    session['carrito'] = []
                    datos['saldo']=saldo
                    with open(path+"datos.json", 'w') as f:
                        f.write(json.dumps(datos))

                    compra = True

                else:
                    no_saldo = True

            else:
                no_registrado = True

    return render_template('carrito.html', title = "Carrito", peliculas=session['carrito'],compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)


@app.route('/carrito/borrar/<valor>')
def carrito_borrar(valor):

    for p in session['carrito']:
        if p['id'] == int(valor):
            session['carrito'].remove(p)
            break

    return redirect(url_for('carrito'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        path = os.path.dirname(__file__)
        path += "/usuarios/"+request.form['username']

        if request.method == 'POST':
            user = request.form['username']
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('userID', user)

        if not isdir(path):
            return render_template('login_registro.html', title = "Log In", existe=True)
        else:
            path += "/"
            datos = json.load(open(path+"datos.json"))
            nombre_usuario=datos['username']
            passw_cif=datos['psw']
            passw = md5(request.form['password'].encode()).hexdigest()
            # aqui se deberia validar con fichero .dat del usuario
            cond = request.form['username'] == nombre_usuario and passw_cif == passw
            if cond:
                session['usuario'] = request.form['username']
                session.modified = True
                if not 'carrito' in session:
                    session['carrito'] = []
                # se puede usar request.referrer para volver a la pagina desde la que se hizo login

                return resp
            else:
                # aqui se le puede pasar como argumento un mensaje de login invalido

                return render_template('login_registro.html', title = "Log In", existe=False)
    else:
        # se puede guardar la pagina desde la que se invoca
        session['url_origen']=request.referrer
        session.modified=True
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer)
        return render_template('login_registro.html', title = "Log In", existe=False)

@app.route('/registro', methods=['GET', 'POST'])
def signup():
    if 'username' in request.form:
        if request.form['password']  == request.form['password2']:
            path = os.path.dirname(__file__)
            path += "/usuarios/"+request.form['username']

            if request.method == 'POST':
                user = request.form['username']
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('userID', user)

            if not isdir(path):
                os.mkdir(path)
                path += "/"
                #historial
                data = {}
                data['pedidos'] = []
                historial =  open(path+"historial.json", "w")
                json.dump(data, historial)
                #datos
                datos = open(path+"datos.json", "w")
                password_cif = md5(request.form['password'].encode()).hexdigest()
                data={}
                data = {
                    'username': request.form['username'],
                    'psw': password_cif,
                    'nombre': request.form['nombre'],
                    'mail': request.form['mail'],
                    'tarjeta': request.form['tarjeta'],
                    'cvc': request.form['cvc'],
                    'saldo': random.randrange(100)
                }
                json.dump(data, datos)
                session['usuario'] = request.form['username']
                session.modified = True

                historial.close()
                return resp
            else:
                return render_template('registro.html', title = "Sign", existe=True)
        else:
            return render_template('registro.html', title = "Sign", existe=False)
    return render_template('registro.html', title = "Sign", existe=False)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    # session.pop('carrito', None)
    return redirect(url_for('index'))
