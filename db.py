import sqlite3

database = 'app.db'

def conectar():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row 
    return conn

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
        create table if not exists usuario (
            id integer primary key autoincrement,
            nome text not null,
            email text unique not null,
            senha text not null
        )
    ''')
    
    cursor.execute('''
        create table if not exists tarefas (
            id integer primary key autoincrement,
            titulo text not null,
            descricao text,
            status text default 'pendente',
            usuario_id integer not null,
            foreign key (usuario_id) references usuario (id) on delete cascade
        )
    ''')
    
    conn.commit()
    conn.close()

def executar_query(query, parametros=()):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, parametros)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def buscar_dados(query, parametros=(), fetchone=False):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(query, parametros)
    
    if fetchone:
        resultado = cursor.fetchone()
    else:
        resultado = cursor.fetchall()
        
    conn.close()
    return resultado

if __name__ == '__main__':
    inicializar_banco()
    print("banco de dados inicializado com sucesso.")