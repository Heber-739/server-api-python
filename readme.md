## Sistema de gestion de tareas
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