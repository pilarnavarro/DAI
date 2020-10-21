from flask import Flask,render_template, request
app = Flask(__name__)
          
import ejercicios as ejers

@app.route('/')
def welcome():
  return 'This is the welcome page!'

#Algorithm es burbuja o merge_sort (también merge)
@app.route('/ordena_matriz/<algorithm>/<lista>')
def ordena(lista,algorithm):
  lista=list(map(int,lista.split(",")))
  return ejers.ordena(lista,algorithm)

@app.route('/criba_eratostenes/<int:number>')
def criba(number):
  message="Los números primos encontrados son:<br/> "
  return message + ejers.criba(number)

@app.route('/fibonacci/<path:input>/<path:output>')
def fibonacci(input,output):
  message="El número de la sucesión de Fibonacci es:<br/> "
  end="<br/> Resultado visible en " + output
  return message + ejers.fibonacci(input,output) + end

@app.route('/balanceo_corchetes', defaults={"cadena": None})
@app.route('/balanceo_corchetes/<cadena>')
def balanceado(cadena):
    if cadena==None:
        cadena="aleatoria" 
    
    if ejers.balanceado(cadena):         
      return "La cadena " + cadena + " está balanceada"
    else:
      return "La cadena " + cadena + " no está balanceada"

@app.route('/expresion_regular/<int:index>/<cadena>')
def regex(index,cadena):
  message="Las subcadenas encontradas con el patrón especificado son:<br/>"
  return message + ejers.regex(index,cadena)


@app.route('/static')
def static_page():
    return app.send_static_file('app.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404