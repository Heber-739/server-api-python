from flask import Flask, request, jsonify, g, abort, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os

DATABASE = 'tareas.db'

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Obtener la conexion a la base de datos (DB)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Inicializa la DB
def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')
    db.commit()

# si no existe la DB la inicializa
if not os.path.exists(DATABASE):
    with app.app_context():
        init_db()

# --- Utils ---

# Metodo para consultas a DB
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv # Retorna el primer valor o todas las coincidencias

# Simula una sesion que se almacena en DB con un ID como token unico
def create_session_for_user(user_id):
    token = str(uuid.uuid4()) 
    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO sessions (user_id, token) VALUES (?, ?)', (user_id, token))
    db.commit()
    return token

# Busca un usuario guardado en la sesion con el token
def get_user_by_token(token):
    row = query_db('SELECT u.* FROM users u JOIN sessions s ON u.id = s.user_id WHERE s.token = ?', (token,), one=True)
    return dict(row) if row else None

# --- Endpoints ---

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    # Verificamos que exista la informacion en la request
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'error': 'Credenciales incorrectas'}), 400

    usuario = data['usuario']
    contraseña = data['contraseña']

    # Creamos el hash a almacenar (unidireccional)
    password_hash = generate_password_hash(contraseña)

    db = get_db()
    try:
        cur = db.cursor()
        cur.execute('INSERT INTO users (usuario, password_hash) VALUES (?, ?)', (usuario, password_hash))
        db.commit()
        # Error que se lanza si tratamos de insertar un usuario ya existente
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El usuario ingresado no es válido'}), 409

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'error': 'Payload invalido'}), 400

    usuario = data['usuario']
    contraseña = data['contraseña']

    row = query_db('SELECT * FROM users WHERE usuario = ?', (usuario,), one=True)
    if row is None:
        return jsonify({'error': 'Credenciales invalidas'}), 401

    user = dict(row)
    if not check_password_hash(user['password_hash'], contraseña):
        return jsonify({'error': 'Credenciales invalidas'}), 401

    token = create_session_for_user(user['id'])
    # Retornamos el token para las request del usuario
    return jsonify({'message': 'Login exitoso', 'token': token}), 200


def require_token(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        #Si no encontramos el token en la request, pedimos que inicie sesion
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Usuario no autenticado en el sistema, por favor inicie sesion'}), 401
        token = auth_header.split(' ', 1)[1]
        user = get_user_by_token(token)
        # Si el usuario no es encontrado, probablemente el token expiró
        if not user:
            return jsonify({'error': 'Token expirado'}), 401
        # añadir usuario al request global
        request.user = user
        return func(*args, **kwargs)
    return wrapper


@app.route('/tareas', methods=['GET'])
@require_token #Usamos nuestro validador como middleware
def tareas():
    user = request.user
    # Obtenemos las tareas almacenadas por el usuario
    rows = query_db('SELECT id, titulo, descripcion FROM tareas WHERE user_id = ?', (user['id'],))
    tareas = [dict(r) for r in rows]

    html = f"""
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <title>Bienvenido</title>
      </head>
      <body>
        <h1>Bienvenido, {user['usuario']}!</h1>
        <p>Tienes {len(tareas)} tarea(s).</p>
        <ul>
    """
    for t in tareas: #iteramos las tareas y las adjuntamos al html
        html += f"<li><strong>{t['titulo']}</strong> - {t['descripcion'] or ''}</li>"
    html += "</ul></body></html>"

    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


# Creamos adicionalmente una opcion para crear las tareas
@app.route('/tareas', methods=['POST'])
@require_token #Usamos nuestro validador como middleware
def crear_tarea():
    data = request.get_json()
    if not data or 'titulo' not in data:
        return jsonify({'error': 'Payload inválido, se requiere "titulo"'}), 400
    titulo = data['titulo']
    descripcion = data.get('descripcion')

    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO tareas (user_id, titulo, descripcion) VALUES (?, ?, ?)', (request.user['id'], titulo, descripcion))
    db.commit()
    return jsonify({'message': 'Tarea creada'}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



