from flask import Flask,render_template
app = Flask(__name__)
          
import ejercicios as ejers

@app.route('/')
def welcome():
  return 'This is the welcome page!'

@app.route('/ordena_matriz')
def ordena():
  return ejers.ordena()

@app.route('/criba_eratostenes')
def criba():
  return ejers.criba()

@app.route('/fibonacci')
def fibonacci():
  return ejers.fibonacci()

@app.route('/balanceo_corchetes')
def balanceado():
  return ejers.balanceado()

@app.route('/expresion_regular/<int:index>')
def regex(index):
  return ejers.regex(index)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404