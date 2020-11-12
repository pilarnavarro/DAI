from flask import Flask,render_template, request, redirect, url_for, flash, session
import ejercicios as ejers
import random
from model import *

app = Flask(__name__)

app.secret_key = 'ys84bba9s7dd5bb308ifas+*jd2384n'


@app.route('/')
def welcome():
  return render_template('base.html')

#Gestión de usuarios y sesiones
@app.route('/signup', methods=['GET','POST'])
def signup():
    error=None
    if request.method == 'POST':
        email = request.form['email']

        if email not in db.keys():
            name = request.form['name']
            password = request.form['password']

            db[email]=dict()
            db[email]['pass']=password
            db[email]['name']=name
            db[email]=db[email]
            
            flash("Usuario " + name + " registrado correctamente. Inicia sesión para empezar a trabajar.")

            return redirect(url_for('welcome'))
        else:
            error='Este email ya esta registrado'

    return render_template('registrarse.html', error=error)

@app.route('/login', methods=['GET','POST'])
def login():
    error=None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in db.keys():
            if db[email]['pass'] == password:
                session['email']=email
                session['name']=db[email]['name']
                #session['urls']=[]
                flash("Sesión iniciada correctamente")
                return redirect(url_for('welcome'))
            else:
                error="Contraseña incorrecta"
        else:
            error="No dispones de una cuenta. Regístrate!"
            return render_template('registrarse.html',error=error)

    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
  if 'email' in session:
    session.clear()
    flash('Ha cerrado sesión correctamente')
  return redirect(url_for('welcome'))

@app.route('/baja')
def baja():
  email=session['email']
  name=db[email]['name']
  db[email].clear()
  del db[email]
  session.clear()
  flash('Usuario '+name+' eliminado correctamente')
  return redirect(url_for('welcome'))

@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
  error = None
  if request.method == 'POST':
    email=session['email']
    if db[email]['pass'] == request.form['password']:
        if request.form['newpass1'] == request.form['newpass2']:
            db[email]['pass'] = request.form['newpass1']
            flash("Contraseña cambiada con éxito")
            return redirect(url_for('welcome'))
        else:
            error = 'Las contraseñas introducidas no coinciden'
    else:
        error = 'Contraseña incorrecta'
  return render_template('new_pass.html', error=error)

@app.after_request
def store_visted_urls(response):
  if 'email' in session:
    if session.get('urls') is None:
      session['urls'] = []   
    session['urls'].append(request.url)
    if len(session['urls']) > 3:
      session['urls'].pop(0)
    session.modified = True
  return response

#Ejercicios práctica 1
@app.route('/adivina', methods=['GET', 'POST'])
def adivina():
  global n,intentos
  if request.method == 'POST':
    if "empezar" in request.form or "nuevo" in request.form:
      n=random.randint(1,100)
      intentos=0
      resultado=-1
    else:
      guess=request.form['numero']
      guess=int(guess)
      intentos=intentos+1

      if n==guess:
        resultado=0
      else:
        if intentos<10:
          if guess>=1 and guess<=100:
            if guess<n:
              resultado=1
            else:
              resultado=2
          else:
            intentos=intentos-1
            resultado=-3
        else:
          resultado=3
    return render_template('ej1.html',intentos=intentos,resultado=resultado)
  
  return render_template('ej1.html',resultado=-2)


@app.route('/criba_eratostenes', methods=['GET', 'POST'])
def criba():
    if request.method == 'POST':
        n = request.form["numero"]
        n = int(n)
        return render_template('criba.html', mostrar=True, n=n, primos=ejers.criba(n))

    return render_template('criba.html', mostrar=False)

@app.route('/balanceo_corchetes', methods=['GET', 'POST'])
def balanceado():
  if request.method == 'POST':
    cadena=request.form["cadena"]
    if ejers.balanceado(cadena):         
      result=True
    else:
      result=False
    return render_template('balanceo.html', mostrar=True, result=result)

  return render_template('balanceo.html', mostrar=False)

@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
  if request.method == 'POST':
        n = request.form["numero"]
        n = int(n)
        return render_template('fib.html', mostrar=True, n=n, salida=ejers.fibonacci(n))

  return render_template('fib.html', mostrar=False)


@app.route('/ordena_matriz', methods=['GET', 'POST'])
def ordena():
  if request.method == 'POST':
    if "burbuja" in request.form:
      algorithm="burbuja"
    if "merge" in request.form:
      algorithm="merge"
  
    lista=request.form["lista"]
    lista=list(map(int,lista.split(",")))
    return render_template('ordena.html', mostrar=True, salida=ejers.ordena(lista,algorithm))
  
  return render_template('ordena.html', mostrar=False)



@app.route('/expresion_regular', methods=['GET', 'POST'])
def regex():
  if request.method == 'POST':
    if "palabra" in request.form:
      index=1
    if "email" in request.form:
      index=2
    if "tarjeta" in request.form:
      index=3
  
    cadena=request.form["texto"]
    
    return render_template('regex.html', mostrar=True, salida=ejers.regex(index,cadena))
  
  return render_template('regex.html', mostrar=False)

#Crear Imágenes Dinámicas
@app.route('/imagen')
def show_figure():
  n = random.randint(0,5)
  if n==0:
    return render_template('rectangle.html')
  elif n==1:
    return render_template('rectangle2.html')
  elif n==2:
    return render_template('circle.html')
  elif n==3:
    return render_template('elipse.html')
  elif n==4:
    return render_template('elipse2.html')
  else:
    return render_template('polygon.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# @app.route('/adivina_init')
# def adivina_init():
#   global n,intentos,resultado
#   n=random.randint(1,100)
#   resultado=-1
#   intentos=0
#   return render_template('ej1.html',intentos=intentos,resultado=resultado)

# @app.route('/adivina', methods=['GET', 'POST'])
# def adivina():
#   global n,intentos,resultado
#   if request.method == 'POST':
#     if "nuevo" in request.form:
#       return redirect(url_for('adivina_init'))
#     else:
#       guess=request.form['numero']
#       guess=int(guess)
#       intentos=intentos+1

#       if n==guess:
#         resultado=0
#       else: 
#         if intentos<10:
#           if guess>=1 and guess<=100:
#             if guess<n:
#               resultado=1
#             else:
#               resultado=2
#           else:
#             intentos=intentos-1
#             resultado=-2
#         else:
#           resultado=3
#   return render_template('ej1.html',intentos=intentos,resultado=resultado)