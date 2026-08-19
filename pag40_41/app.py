import os
from functools import wraps
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import inicializar_banco, buscar_dados, executar_query

app = Flask(__name__)


app.secret_key = os.environ.get('SECRET_KEY', 'chave_dev_mude_em_producao')

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

inicializar_banco()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/tarefas')
@login_required
def api_tarefas():
    usuario_id = session['usuario_id']
    status = request.args.get('status', 'todas')
    
    if status in ['pendente', 'em_andamento', 'concluida']:
        tarefas = buscar_dados(
            "select id, titulo, descricao, status from tarefas where usuario_id = ? and status = ? order by id desc",
            (usuario_id, status)
        )
    else:
        tarefas = buscar_dados(
            "select id, titulo, descricao, status from tarefas where usuario_id = ? order by id desc",
            (usuario_id,)
        )
        
    return jsonify([dict(t) for t in tarefas])

@app.route('/api/estatisticas')
@login_required
def api_estatisticas():
    usuario_id = session['usuario_id']
    
    pendentes = buscar_dados("select count(*) as total from tarefas where usuario_id = ? and status = 'pendente'", (usuario_id,), fetchone=True)['total']
    em_andamento = buscar_dados("select count(*) as total from tarefas where usuario_id = ? and status = 'em_andamento'", (usuario_id,), fetchone=True)['total']
    concluidas = buscar_dados("select count(*) as total from tarefas where usuario_id = ? and status = 'concluida'", (usuario_id,), fetchone=True)['total']
    
    return jsonify({
        'pendente': pendentes,
        'em_andamento': em_andamento,
        'concluida': concluidas
    })


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/progresso')
@login_required
def progresso():
    return render_template('progresso.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        if not nome or len(nome) < 2:
            flash('Informe um nome válido.', 'danger')
            return redirect(url_for('registro'))
        if not email or '@' not in email:
            flash('Informe um e-mail válido.', 'danger')
            return redirect(url_for('registro'))
        if not senha or len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
            return redirect(url_for('registro'))

        usuario_existente = buscar_dados("select id from usuario where email = ?", (email,), fetchone=True)
        if usuario_existente:
            flash('Este email já está cadastrado.', 'danger')
            return redirect(url_for('registro'))

        senha_hash = generate_password_hash(senha)
        executar_query("insert into usuario (nome, email, senha) values (?, ?, ?)", (nome, email, senha_hash))
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

if __name__ == '__main__':
    modo_debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=modo_debug)