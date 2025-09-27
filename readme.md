# [Repositorio Github](https://github.com/Heber-739/server-api-python)

```bash
https://github.com/Heber-739/server-api-python
``` 

# Sistema de gestion de tareas
### Requisitos

- Python 3.8
- Postman o similar

### Pasos de prueba
1 - Descargar los archivos e instalar las dependencias
```bash
pip install flask requests
```

2 - Ejecutar el archivo `servidor.py`

```bash
python servidor.py
```
El servidor arrancará en [http://127.0.0.1:5000](http://127.0.0.1:5000)


## Ejecutar la linea de comandos
Permitirá el uso del server

```bash
python cliente.py
```

## Pruebas por postman
### Registrar un usuario (ejemplo curl)

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"usuario":"juan","contraseña":"miPass123"}' \
  http://127.0.0.1:5000/registro
```

Respuesta esperada: `201` y mensaje `Usuario registrado`.

### Login y obtención de token

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"usuario":"juan","contraseña":"miPass123"}' \
  http://127.0.0.1:5000/login
```

Respuesta: `200` con `{"token":"..."}`.

### Acceder a /tareas (HTML)

Usando curl (reemplazar <TOKEN>):

```bash
curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5000/tareas
```

Se devolverá un HTML con bienvenida y la lista de tareas del usuario.

### Crear tarea (POST /tareas)

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" \
  -d '{"titulo":"Comprar leche","descripcion":"Ir al supermercado"}' \
  http://127.0.0.1:5000/tareas
```

#Respuestas Conceptuales
## Por qué hashear contraseñas?

Guardar contraseñas tal cual las escribe el usuario es extremadamente inseguro, si la BD es robada o accedida, las contraseñas no pueden leerse directamente, porque el hash es un resultado irreversible (unidireccional). Los algoritmos de hashing (bcrypt por ejemplo) están diseñados para que no se pueda obtener la contraseña original a partir del hash.
Por lo que es mas seguro la comparacion de los hash de las contraseñas que el texto plano ingresado por el usuario. Esto es, almacenar el hash de la contraseña en DB, y cuando el usuario intente loguearse, hacer el hash del input y compararlo con el almacenado.


## Ventajas de usar SQLite

No requiere instalar ni administrar un servidor (como MySQL o PostgreSQL). Esto la vuelve más liviana y mejora la usabilidad.

Python incluye el módulo sqlite3 en la librería estándar, sin dependencias extra.

Es perfecta para prototipos, pruebas locales y aplicaciones de bajo tráfico. Ideal para proyectos pequeños

LA implementacion de esta BD con SQLite fue tan rapida como instalar la libreria y ejecutar los comandos. Sin programas extras ni procesos extras.