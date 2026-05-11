from flask import Flask

app = Flask(__name__)

@app.route('/')
def oq_e_flask():
    return "Um decorator em Python é uma função que modifica ou estende o comportamento de outra função, método ou classe sem alterar seu código-fonte original.\n Os decoradores (decorators) em Python servem para modificar ou estender o comportamento de funções, métodos ou classes sem alterar seu código-fonte original.\n Decoradores no Flask são usados para adicionar funcionalidades a funções de visualização (views) sem alterar seu código original, sendo representados pela sintaxe @nome_do_decorator acima da definição da função. O exemplo principal é @app.route(), que associa uma URL à função, transformando-a em uma rota acessível " 
    

if __name__ == '__main__':
    app.run(debug=True)