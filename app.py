from flask import Flask, render_template, request
from calculadora import calcular 

app = Flask(__name__)

@app.route('/')
def inicial():
     if request.method == 'POST': 
        return calcular
     return render_template('calculadora.html', etapas ='', resultados = '')

@app.route('/calcular', methods=['POST'])
def calcular_route(): 
    return calcular()

if __name__ == "__main__":
    app.run(debug=True)