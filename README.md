# Proyecto FastAPI con PostgreSQL

Este proyecto incluye una aplicación FastAPI y una base de datos PostgreSQL. Las instrucciones a continuación son para configurar un entorno virtual, instalar las dependencias y ejecutar la aplicación.

## Requisitos

- Python 3.8 o superior
- `virtualenv` (o `poetry`)
- Docker (para ejecutar la aplicación con Docker Compose)

## Crear y activar un entorno virtual con `virtualenv`

### Linux (Bash)

1. **Instalar `virtualenv`** (si no lo tienes instalado):
   ```sh
   pip install virtualenv
   ```
2. **Crear entorno virtual**:
   ```sh
   virtualenv env
   ```
3. **Activar entorno virtual**:
   ```sh
   source venv/bin/activate
   ```
4. **Instalar dependencias**:
   ```sh
   pip install -r requirements.txt
   ```

### Windows (Powershell)

1. **Instalar `virtualenv`** (si no lo tienes instalado):
   ```sh
   pip install virtualenv
   ```
2. **Crear entorno virtual**:
   ```sh
   virtualenv env
   ```
3. **Activar entorno virtual**:
   ```sh
   .\env\Scripts\activate.ps1
   # Tambien puede aparecer como .\env\bin\Scripts\activate.ps1

   ```
4. **Instalar dependencias**:
   ```sh
   pip install -r requirements.txt
   ```


## Crear y activar un entorno virtual con `poetry`

**Primero asegurese que tenga instalado `poetry`**

### Cualquier SO (Linux, Windows, Mac)

1. **Inicializar un proyecto con `poetry`**:
```sh
poetry init
```
Siga las instrucciones que indique `poetry` para configurar su `pyproject.toml`

2. Copiar el archivo `poetry.lock` dentro del proyecto generado con `poetry`
3. **Instalar las dependencias**L Ejecutar `poetry install`

## Ejecutar la aplicación

Después de activar el entorno virtual y de instalar las dependencias, puedes ejecutar la aplicación FastAPI utilizando `uvicorn` (tambien funciona en un entorno generado por `poetry`):
```sh
uvicorn src.main:app --reload
```

Si esta usando `poetry`, otra opcion puede ser: `poetry run uvicorn src.main:app --reload`

La aplicación estará disponible en `http://127.0.0.1:8000` o `http://localhost:8000`

En la ruta `/docs` tiene disponible la interfaz de SwaggerUI

**La aplicación no se ejecutará si no tiene las variables de entorno definidas**, pero está configurada para ejecutarse con un archivo llamado `.env.local` que apunta a una base de datos de pruebas de PostgreSQL en la nube, puede revisar este archivo para saber cuales son.


## Ejecutar con `docker-compose`

Para ejecutar la aplicación y la base de datos PostgreSQL usando `docker-compose`, primero tiene que tener instalado Docker y docker-compose:
```sh
docker-compose up --build
```
La aplicación estará disponible en http://localhost:8000

## Ejecutar las migraciones con `alembic`

Para aplicar las migraciones incrementales de bases de datos, ejecute

```sh
alembic upgrade head
```
**Nota**: utiliza la variable de entorno `POSTGRES_DSN`, en un ambiente de testing no hace falta utilizar `alembic`, si necesita aplicar los esquemas en una base de datos de prueba, va a necesitar linkear una URI

## Ejecutar los tests
Los tests estan creados con `pytest`, para ejecutar todos los tests, ejecute el siguiente comando:
```sh
pytest -vvvv
```
No hace falta conectarse a una base de datos para correr los tests porque crea una base de datos SQLite3 en memoria.

## Variables de entorno

Para ejecutar correctamente este proyecto, necesita agregar las siguientes variables de entorno:

`POSTGRES_DSN`: URI para conectarse a la base de datos, en el ambiente de testing no hace falta ya que ejecuta una base de datos SQLite3 en memoria, si está ejecutando la aplicacion en local o en un ambiente de testing, puede utilizar el archivo `.env.local` y apuntar a una base de datos PostgreSQL

`JWT_PRIVATE_KEY`: Frase para la firma de los tokens JWT, si o si se necesita para cualquier ambiente, si esta en el ambiente local o de testing, puede utilizar el archivo `.env.local`

## Docker image

La imagen de Docker esta subida [aqui](https://hub.docker.com/repository/docker/facundopadilla/n5now/general).

## Servicios de AWS

Para crear una base de datos PostgreSQL y desplegar una aplicación FastAPI en Amazon Web Services (AWS), se puede utilizar los siguientes servicios:
- **Amazon RDS (para PostgreSQL)**: Este servicio te permite configurar, operar y escalar una base de datos PostgreSQL en la nube.
- **Para el deploy**: hay varias opciones como Amazon EC2 (si se necesita un entorno controlado, **que sea persistente** y si va a administrar todo), AWS Lambda (si no necesita un servidor, son tareas intermitentes y prefiere pagar por uso), AWS Fargate (parecido a Lambda, pero utiliza contenedores de Docker), una buena opcion general podria ser Fargate por la ventaja de reutilizar dockerfiles y no tener necesidad de administrar la infraestructura, pero si es una aplicacion con servicios persistentes usaria EC2, y si fuese una aplicacion con funciones "intermitentes" (un microservicio que se utiliza para cosas especificas y de manera esporadica/intermitente), usaria Lambda.