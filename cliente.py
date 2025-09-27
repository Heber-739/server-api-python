
import requests
import sys

BASE = 'http://127.0.0.1:5000'


def registro(usuario, contraseña):
    r = requests.post(BASE + '/registro', json={'usuario': usuario, 'contraseña': contraseña})
    print(r.status_code, r.text)


def login(usuario, contraseña):
    r = requests.post(BASE + '/login', json={'usuario': usuario, 'contraseña': contraseña})
    print(r.status_code, r.text)
    if r.status_code == 200:
        return r.json().get('token')


def ver_tareas(token):
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(BASE + '/tareas', headers=headers)
    if r.status_code == 200:
        print('\n--- Página HTML recibida ---\n')
        print(r.text[:1000])
    else:
        print(r.status_code, r.text)

def crear_tarea(token, titulo, descripcion=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {'titulo': titulo}
    if descripcion:
        data['descripcion'] = descripcion

    r = requests.post(BASE + '/tareas', headers=headers, json=data)
    print(r.status_code, r.text)

if __name__ == '__main__':
    import getpass
    print('---------- Cliente CLI ---------- ')
    cmd = input('comando (registro/login/ver/crear): ').strip()
    if cmd == 'registro':
        usuario = input('usuario: ')
        contraseña = getpass.getpass('contraseña: ')
        registro(usuario, contraseña)
    elif cmd == 'login':
        usuario = input('usuario: ')
        contraseña = getpass.getpass('contraseña: ')
        token = login(usuario, contraseña)
        if token:
            print('Token:', token)
    elif cmd == 'ver':
        token = input('Token: ')
        ver_tareas(token)
    elif cmd == 'crear':
        token = input('Token: ')
        titulo = input('Título de la tarea: ')
        descripcion = input('Descripción (opcional): ')
        crear_tarea(token, titulo, descripcion or None)
    else:
        print('Opcion no reconocida')

