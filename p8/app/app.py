from flask import Flask,render_template, request, redirect, url_for, flash, session, jsonify
from bson import ObjectId
import ejercicios as ejers
import random
from model import *


app = Flask(__name__)

app.secret_key = 'ys84bba9s7dd5bb308ifas+*jd2384n'


@app.route('/p8')
def p8():
  return render_template('p8.html')

@app.route('/')
def welcome():
  return render_template('base.html')

#Práctica 5 - API REST
@app.route('/api/episodios', methods=['GET','POST'])
def api_1():
  if request.method == 'GET':
    numerico=["season","id","number","runtime"]
    condiciones=[]
    for key in request.values.keys():
      if key in numerico:
        condiciones.append({key:float(request.values.get(key))})
      else:
        condiciones.append({key:{"$regex":request.values.get(key),"$options":'i'}})
    
    if len(condiciones)!=0:
      episodios = db2.samples_friends.find({"$and":condiciones}) 
    else:
      episodios = db2.samples_friends.find()
    
    lista_episodios = []
    for episodio in episodios:
      identificador=str(episodio.get('_id'))
      del episodio["_id"]
      episodio["id2"]=episodio["id"]
      del episodio["id"]
      lista_episodios.append({**episodio, "id":identificador})
    if len(lista_episodios)==0:
      return jsonify({'error':'No se ha encontrado ninguna entrada con las caracteristicas introducidas'}), 404
    return jsonify(lista_episodios)
  
  if request.method == 'POST':
    iden=request.form.get('id')
    if iden!=None:
      iden=float(iden)
      if db2.samples_friends.find_one({"id":iden})!=None:
        return jsonify({'error':'Ya existe una entrada con este id'}), 400
      else:
        entrada={}
        numerico=["season","id","number","runtime"]
        for key in request.values.keys():
          if key in numerico:
            entrada[key]=float(request.values.get(key))
          else:
            entrada[key]=request.values.get(key)

        new_id=db2.samples_friends.insert_one(entrada).inserted_id
        episodio = db2.samples_friends.find_one({"id":iden}, {"_id": 0})
        episodio["id2"]=episodio["id"]
        del episodio["id"]

        return jsonify({**episodio, "id": str(new_id)})
    else:
      return jsonify({'error':'La nueva entrada debe incluir un id'}), 400
      
@app.route('/api/episodios/<identificador>', methods=['GET','PUT','DELETE'])
def api_2(identificador):
  try:
    resultado=db2.samples_friends.find_one({"_id":ObjectId(identificador)},{"_id":0})
  except:
    return jsonify({'error':'Not found'}), 404
  
  if resultado==None:
    return jsonify({'error':'No existe ninguna entrada con este id'}), 404

  if request.method == 'GET':
    resultado["id2"]=resultado["id"]
    del resultado["id"]
    return jsonify({**resultado, "id": identificador})

  if request.method == 'DELETE':
    db2.samples_friends.delete_one({'_id':ObjectId(identificador)}) 
    return jsonify({"id": identificador})
  
  if request.method == 'PUT':
    #Poner name==paco, dos =, al pasar los argumentos en el PUT con httpie
    numerico=["season", "number","runtime"]
    for key in request.values.keys():
      if key=="id":
        return jsonify({'error':'No se puede modificar el campo id'}), 400
      elif key in numerico:
        db2.samples_friends.update(
            {"_id":ObjectId(identificador)},
            {"$set":{key:float(request.values.get(key))}}
          )
      else:
        db2.samples_friends.update(
            {"_id":ObjectId(identificador)},
            {"$set":{key:request.values.get(key)}}
          )
    
    episodio=db2.samples_friends.find_one({"_id":ObjectId(identificador)},{"_id": 0})
    episodio["id2"]=episodio["id"]
    del episodio["id"]

    return jsonify({**episodio, "id": identificador})

#------------------------------------------------------------
#Práctica 4 - MongoDB
@app.route('/mongo', methods=['GET','POST'])
def mongo():
  episodios = db2.samples_friends.find() 
  lista_episodios = []
  for episodio in episodios:
    #app.logger.debug(episodio) 
    lista_episodios.append(episodio)

    if request.method == 'POST':
      if "nuevo" in request.form:
        return redirect(url_for('mongo_insertar'))
      if "borrar" in request.form:
        return redirect(url_for('mongo_eliminar'))
      if "mod" in request.form:
        return redirect(url_for('mongo_modificar'))
      if "buscar" in request.form:
        return redirect(url_for('mongo_buscar'))

  return render_template('lista_db.html', episodios=lista_episodios)

@app.route('/mongo/insertar', methods=['GET','POST'])
def mongo_insertar():
  if request.method == 'POST':
    iden=request.form['iden']
    iden=float(iden)
    if db2.samples_friends.find_one({"id":iden})!=None:
      flash("Ya existe una entrada con este id")
      return render_template('insertar_db.html')
    else:
      name=request.form['name']
      url=request.form['url']
      season=request.form['season']
      number=request.form['number']
      airdate=request.form['airdate']
      airtime=request.form['airtime']
      airstamp=request.form['airstamp']
      runtime=request.form['runtime']
      summary=request.form['summary']

      entrada={"id":iden,"url":url,"name":name,"season":season,"number":number,"airdate":airdate,
      "airtime":airtime,"airstamp":airstamp,"runtime":runtime,"summary":summary}

      db2.samples_friends.insert_one(entrada)

      flash("Entrada creada e insertada correctamente")
      return redirect(url_for('mongo')) 
  return render_template('insertar_db.html')

@app.route('/mongo/eliminar', methods=['GET','POST'])
def mongo_eliminar():
  if request.method == 'POST':
    name=request.form['name']
    result=db2.samples_friends.delete_many( {"name":name} ) 
    if result.deleted_count==0:
      flash("No hay ningún episodio con ese nombre. Inténtelo de nuevo")
      return render_template('eliminar_db.html')
    else:
      flash("Entrada eliminada correctamente")
    return redirect(url_for('mongo')) 
  return render_template('eliminar_db.html')

@app.route('/mongo/modificar', methods=['GET','POST'])
def mongo_modificar():
  if request.method == 'POST':
    iden=request.form['iden']
    iden=float(iden)
    if db2.samples_friends.find_one({"id":iden})!= None:
      propiedades=["url","name","season","number","airdate","airtime","airstamp","runtime","summary"]
      for i in range(len(propiedades)):
        if len(request.form[propiedades[i]])!=0:
          db2.samples_friends.update(
            {"id":iden},
            {"$set":{propiedades[i]:request.form[propiedades[i]]}}
          )
      flash("Entrada modificada correctamente")
      return redirect(url_for('mongo')) 
    else:
      flash("No existe ninguna entrada con el id especificado")
      return render_template('modificar_db.html')
    
  return render_template('modificar_db.html')

@app.route('/mongo/consultar', methods=['GET','POST'])
def mongo_buscar():
  if request.method == 'POST':
      propiedades=["id","url","name","season","number","airdate","airtime","airstamp","runtime","summary"]
      condiciones=[]
      for i in range(len(propiedades)):
        if len(request.form[propiedades[i]])!=0:
          if propiedades[i]=="season" or propiedades[i]=="id" or propiedades[i]=="number" or propiedades[i]=="runtime":
            propiedad=float(request.form[propiedades[i]])
            condiciones.append({propiedades[i]:propiedad})
          else:
            propiedad=request.form[propiedades[i]]
            condiciones.append({propiedades[i]:{"$regex":propiedad,"$options":'i'}})
          
      episodios = db2.samples_friends.find({"$and":condiciones}) 
      lista_episodios = []
      for episodio in episodios:
        lista_episodios.append(episodio)
      if len(lista_episodios)==0:
        flash("No se ha encontrado ningún episodio con las características introducidas")
      else:
        return render_template('consultar_db.html',mostrar=True,episodios=lista_episodios)
    
  return render_template('consultar_db.html',mostrar=False)

#------------------------------------------------------------
#Práctica 3

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
