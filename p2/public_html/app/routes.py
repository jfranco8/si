#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys
from hashlib import md5
import random
from os.path import isdir
import time

@app.route('/')

#pagina de inicio
@app.route('/index')
def index():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Todas las muuuvies", movies=catalogue['peliculas'])

#tipos de pelis
@app.route('/<tipo>')
def todas(tipo):
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    pelis = []
    titulo="Nada"
    if tipo=="novedades":
        titulo="Novedades"
        for p in catalogue['peliculas']:
            if p['novedades'] == True:
                pelis.append(p)
    elif tipo=="masvistas":
        titulo="Muuuvies mas vistas"
        for p in catalogue['peliculas']:
            if p['mas_vistas'] == True:
                pelis.append(p)
    else:
        pelis = catalogue['peliculas']
        titulo="Todas las muuuvies"
    return render_template('index.html', title = titulo, movies=pelis)

#categorias de pelis
@app.route('/categorias/<cat>')
def categorias(cat):
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
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
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    for p in catalogue['peliculas']:
        if p['id'] == int(valor):
            if request.method == 'POST':
                if not "carrito" in session:
                    session["carrito"] = []
                session["carrito"].append(p)
            return render_template('pelicula.html', title = p['titulo'], pelicula=p)
    return redirect(url_for('index'))

#busqueda de peli
@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
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
    datos = open(path+usuario+".dat", "r")
    dat = []
    username=datos.readline().rstrip('\n') #nombre de usuario
    passw=datos.readline().rstrip('\n') #ps
    name=datos.readline().rstrip('\n') #nombre
    mail=datos.readline().rstrip('\n') #mail
    card=datos.readline().rstrip('\n') #tarjeta
    cvc=datos.readline().rstrip('\n') #cvc
    saldo=datos.readline().rstrip('\n') #saldo
    datos.close()
    if request.method == 'POST':
        old_contr = request.form['old']
        new_contr1 = request.form['new1']
        new_contr2 = request.form['new2']

        if md5(old_contr.encode()).hexdigest() != passw:
            return render_template('cambiar_contrasena.html', title = "Cambiar contraseña", mal=True)

        datos = open(path+usuario+".dat", "w")
        datos.write(username+"\n")
        password_cif = md5(new_contr1.encode()).hexdigest()
        datos.write(password_cif+"\n")
        datos.write(name+"\n")
        datos.write(mail+"\n")
        datos.write(card+"\n")
        datos.write(cvc+"\n")
        datos.write(saldo) #saldo
        return redirect(url_for('index'))
    return render_template('cambiar_contrasena.html', title = "Cambiar contraseña", mal=False)


@app.route('/perfil/<usuario>/', methods=['GET', 'POST'])
def perfil(usuario):
    path = os.path.dirname(__file__)
    path += "/usuarios/"+usuario+"/"
    datos = open(path+usuario+".dat", "r")
    dat = []
    username=datos.readline().rstrip('\n') #nombre de usuario
    passw=datos.readline().rstrip('\n') #ps
    name=datos.readline().rstrip('\n') #nombre
    mail=datos.readline().rstrip('\n') #mail
    card=datos.readline().rstrip('\n') #tarjeta
    cvc=datos.readline().rstrip('\n') #cvc
    saldo=datos.readline().rstrip('\n') #saldo
    error = False
    datos.close()

    if request.method == 'POST':
        saldo_new = request.form['saldo_nuevo']
        if float(saldo_new) < 0:
            error = True
        else:
            saldo = float(saldo) + float(saldo_new)
        datos = open(path+usuario+".dat", "w")
        datos.write(username+"\n")
        datos.write(passw+"\n")
        datos.write(name+"\n")
        datos.write(mail+"\n")
        datos.write(card+"\n")
        datos.write(cvc+"\n")
        datos.write(str(saldo)) #saldo

    return render_template('perfil.html', name=name, passw=passw, username=username,
        mail=mail, card=card, saldo=saldo, error=error)


@app.route('/historial',methods=['GET', 'POST'])
def historial():
    path = os.path.dirname(__file__)
    path += "/usuarios/"+session['usuario']+"/historial.json"
    historial = json.load(open(path))['peliculas']
    fechas = []
    for p in historial:
        if not p['fecha'] in fechas:
            fechas.append(p['fecha'])
    return render_template('historial.html', title = "Historial", peliculas=historial, username=session['usuario'], fechas=fechas)

@app.route('/historial/<valor>',methods=['GET', 'POST'])
def historial_fecha(valor):
    path = os.path.dirname(__file__)
    path += "/usuarios/"+session['usuario']+"/historial.json"
    historial = json.load(open(path))['peliculas']
    fechas = []
    peliculas = []
    for p in historial:
        if not p['fecha'] in fechas:
            fechas.append(p['fecha'])
        if p['fecha'] == valor:
            peliculas.append(p)
    return render_template('historial.html', title = "Historial", peliculas=peliculas, username=session['usuario'], fechas=fechas)


@app.route('/carrito', methods=['GET', 'POST'])
def carrito():

    no_saldo = False
    no_registrado = False
    compra = False

    if not "carrito" in session:
        session["carrito"] = []


    if request.method == 'POST':

        if session["carrito"] != []:

            if 'usuario' in session:

                path = os.path.dirname(__file__)
                path += "/usuarios/"+session['usuario']+"/"
                datos = open(path+session['usuario']+".dat", "r")
                dat = []
                username=datos.readline().rstrip('\n') #nombre de usuario
                passw=datos.readline().rstrip('\n') #ps
                name=datos.readline().rstrip('\n') #nombre
                mail=datos.readline().rstrip('\n') #mail
                card=datos.readline().rstrip('\n') #tarjeta
                cvc=datos.readline().rstrip('\n') #cvc
                saldo=float(datos.readline().rstrip('\n')) #saldo
                datos.close()
                coste = 0

                for p in session["carrito"]:
                    coste += float(p['precio'])

                if float(coste) <= float(saldo):
                    saldo -= coste

                    data = json.load(open(path+'historial.json'))
                    for p in session["carrito"]:
                        peli = {
                            'pelicula' : p,
                            'fecha'   :  time.strftime("%d.%m.%Y")
                        }
                        data['peliculas'].append(peli)

                    with open(path+'historial.json', 'w') as file:
                        json.dump(data, file)

                    session["carrito"] = []
                    datos = open(path+session['usuario']+".dat", "w")
                    datos.write(username+"\n")
                    datos.write(passw+"\n")
                    datos.write(name+"\n")
                    datos.write(mail+"\n")
                    datos.write(card+"\n")
                    datos.write(cvc+"\n")
                    datos.write(str(saldo)) #saldo

                    compra = True

                else:
                    no_saldo = True

            else:
                no_registrado = True

    return render_template('carrito.html', title = "Carrito", peliculas=session["carrito"],compra=compra, no_saldo=no_saldo, no_registrado=no_registrado)


@app.route('/carrito/borrar/<valor>')
def carrito_borrar(valor):

    for p in session["carrito"]:
        if p['id'] == int(valor):
            session["carrito"].remove(p)
            break

    return redirect('/carrito')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        path = os.path.dirname(__file__)
        path += "/usuarios/"+request.form['username']
        if not isdir(path):
            return render_template('login_registro.html', title = "Log In", existe=True)
        else:
            path += "/"
            datos = open(path+request.form['username']+".dat", "r")
            nombre_usuario=datos.readline().rstrip('\n')
            passw_cif=datos.readline().rstrip('\n')
            passw = md5(request.form['password'].encode()).hexdigest()
            print(nombre_usuario+passw)
            # aqui se deberia validar con fichero .dat del usuario
            cond = request.form['username'] == nombre_usuario and passw_cif == passw
            print(cond)
            if cond:
                session['usuario'] = request.form['username']
                session.modified = True
                if not "carrito" in session:
                    session["carrito"] = []
                # se puede usar request.referrer para volver a la pagina desde la que se hizo login
                datos.close()
                return redirect(url_for('index'))
            else:
                # aqui se le puede pasar como argumento un mensaje de login invalido
                datos.close()
                return render_template('login_registro.html', title = "Log In", existe=False)
    else:
        # se puede guardar la pagina desde la que se invoca
        session['url_origen']=request.referrer
        session.modified=True
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login_registro.html', title = "Log In", existe=False)

@app.route('/registro', methods=['GET', 'POST'])
def signup():
    if 'username' in request.form:
        if request.form['password']  == request.form['password2']:
            path = os.path.dirname(__file__)
            path += "/usuarios/"+request.form['username']
            if not isdir(path):
                os.mkdir(path)
                path += "/"
                datos = open(path+request.form['username']+".dat", "w")
                data = {}
                data['peliculas'] = []
                historial =  open(path+"historial.json", "w")
                json.dump(data, historial)
                datos.write(request.form['username']+"\n")
                password_cif = md5(request.form['password'].encode()).hexdigest()
                datos.write(password_cif+"\n")
                #datos.write(request.form['password']+"\n")
                datos.write(request.form['nombre']+"\n")
                datos.write(request.form['mail']+"\n")
                datos.write(request.form['tarjeta']+"\n")
                datos.write(request.form['cvc']+"\n")
                datos.write(str(random.randrange(100))) #saldo
                session['usuario'] = request.form['username']
                session.modified = True
                datos.close()
                historial.close()
                return redirect(url_for('index'))
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
