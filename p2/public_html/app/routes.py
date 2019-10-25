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
    else:
        titulo="Ciencia ficcion"
    for p in catalogue['peliculas']:
        for c in p['categorias']:
            if c['cat'] == titulo:
                pelis.append(p)
    return render_template('index.html', title = titulo, movies=pelis)

#peli concreta
@app.route('/pelicula/<valor>/')
def pelicula(valor):
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
    catalogue = json.loads(catalogue_data)
    for p in catalogue['peliculas']:
        if p['id'] == int(valor):
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

@app.route('/perfil/<usuario>', methods=['GET', 'POST'])
def perfil(usuario):
    if "user" in session:
        if user != usuario:
            return redirect(url_for('index'))
        path = os.path.dirname(__file__)
        path += "/usuarios/"+request.form[usuario]+"/"
        datos = open(path+request.form['username']+".dat", "r")
        dat[0]=datos.readline().rstrip('\n') #id
        passw_cif=datos.readline().rstrip('\n') #ps
        dat[1]=datos.readline().rstrip('\n') #nombre
        dat[2]=datos.readline().rstrip('\n') #mail
        dat[3]=datos.readline().rstrip('\n') #tarjeta
        cvc=datos.readline().rstrip('\n') #cvc
        dat[4]=datos.readline().rstrip('\n') #saldo
    return render_template('perfil.html', valores=dat)
    return render_template('perfil.html')

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
                return redirect(url_for('index'))
            else:
                return render_template('registro.html', title = "Sign", existe=True)
        else:
            return render_template('registro.html', title = "Sign", existe=False)
    return render_template('registro.html', title = "Sign", existe=False)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))
