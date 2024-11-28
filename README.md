# PREMIOS / AWARDS

Este repositorio automatiza la carga de datos de diversos premios a **MongoDB Atlas** utilizando **GitHub Actions**. Los datos son extraídos de APIs relacionadas con los premios más importantes del mundo: **Balones de Oro**, **Premios Nobel**, **Premios Oscar**, y **Premios Cervantes**. Los flujos de trabajo de GitHub Actions permiten que los datos se suban a MongoDB Atlas automáticamente con cada actualización del código.

## Cómo Funciona

Cada vez que se hace un **push** a la rama `main`, los siguientes flujos de trabajo se activan:

### 1. Subir Balones de Oro
Se ejecuta el script `cargarBalonesDeOro.py` para cargar los datos de los **Balones de Oro** a MongoDB Atlas.

### 2. Subir Premios Nobel
Se ejecuta el script `cargarPremiosNobel.py` para cargar los datos de los **Premios Nobel** a MongoDB Atlas.

### 3. Subir Premios Oscar
Se ejecuta el script `cargarPremiosOscar.py` para cargar los datos de los **Premios Oscar** a MongoDB Atlas.

### 4. Subir Premios Cervantes
Se ejecuta el script `cargarPremiosCervantes.py` para cargar los datos de los **Premios Cervantes** a MongoDB Atlas.

## Requisitos

- **MongoDB Atlas**: Necesitas una cuenta en MongoDB Atlas y configurar una URI de conexión en los secretos del repositorio bajo el nombre `MONGO_URI`.
- **GitHub Actions**: Se utiliza para automatizar los flujos de trabajo.

### Librerías necesarias

En el archivo `requirements.txt` se encuentran las dependencias necesarias para que el proyecto funcione correctamente. Estas son:

- **requests**: Esta librería es utilizada para hacer solicitudes HTTP. En este proyecto, se usa para interactuar con las APIs de los premios, obteniendo datos de ellos mediante peticiones web.
- **pymongo**: Es el driver de Python para MongoDB, y se utiliza para conectar y trabajar con **MongoDB Atlas**. Esta librería permite insertar, actualizar y consultar los datos de los premios en la base de datos MongoDB.
- **python-dotenv**: Esta librería se utiliza para cargar variables de entorno desde un archivo `.env`. En este proyecto, es útil para almacenar de manera segura información sensible como la URI de conexión de MongoDB Atlas.
- **beautifulsoup4**: Esta librería facilita el parseo de contenido HTML y XML. En este caso, se usa para extraer datos de las páginas web de los premios, como los ganadores o las categorías.

Estas dependencias son fundamentales para el correcto funcionamiento de la automatización de la carga de datos a **MongoDB Atlas** a través de **GitHub Actions**.

## Configuración de MongoDB Atlas

1. **Crea una cuenta** en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) y configura una base de datos.
2. **Configura el acceso de red**: Ve a **Network Access** y agrega la IP `0.0.0.0/0` para permitir conexiones desde cualquier red, incluyendo GitHub Actions.
3. **Configura la URI de conexión** en los **secretos** de GitHub bajo el nombre `MONGO_URI`.

## Instalación

### Configura los secretos en GitHub:

1. Agrega la URI de conexión de MongoDB Atlas como un secreto llamado `MONGO_URI`.

### Instalar dependencias:

Si deseas ejecutar el proyecto localmente, instala las dependencias necesarias con el siguiente comando:

```bash
pip install -r requirements.txt
pip install beautifulsoup4
