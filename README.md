# API de Premios Oscar

## Descripción

Este proyecto permite acceder a una API que ofrece información sobre los Premios Oscar. Para configurarlo y comenzar a usarlo, sigue los pasos a continuación.

---

## Pasos para Configurar la API

### 1. **Registrarse en Ngrok**
   - Dirígete a [Ngrok](https://ngrok.com/) y regístrate para obtener una cuenta gratuita.

### 2. **Instalar Ngrok**
   - Descarga Ngrok desde [este enlace](https://download.ngrok.com/windows?tab=download) y sigue las instrucciones de instalación para tu sistema operativo.

### 3. **Obtener tu Token de Ngrok**
   - Después de registrarte, dirígete a [este enlace](https://dashboard.ngrok.com/get-started/your-authtoken) y copia tu token de Ngrok.

### 4. **Configurar el Archivo `main.py`**
   - Abre el archivo `main.py` en tu editor de Visual Studio.
   - Abre la terminal de Visual Studio y ejecuta el siguiente comando para desplegar la API:

     ```bash
     uvicorn main:app
     ```

   - Esto hará que la API se despliegue en `localhost`.

---

## Configurar Ngrok en tu Sistema

### 1. **Configurar Variables de Entorno**
   - Pulsa `Windows + R`, escribe `sysdm.cpl` y presiona Enter.
   - Ve a **Opciones Avanzadas** y luego a **Variables de entorno**.
   - En **Variables de sistema**, selecciona `Path` y haz clic en **Editar**.
   - Añade un nuevo path con la ruta donde se encuentre el archivo `ngrok.exe` en tu sistema.

### 2. **Verificar la Instalación de Ngrok**
   - Abre la terminal o el CMD de Windows y ejecuta el siguiente comando para verificar que Ngrok está correctamente instalado:

     ```bash
     ngrok version
     ```

   - Esto debería mostrar la versión de Ngrok instalada.

### 3. **Activar tu Token de Ngrok**
   - En el CMD de Windows, ejecuta el siguiente comando para activar tu token de Ngrok (reemplaza `<tu_token_aqui>` con el token que copiaste anteriormente):

     ```bash
     ngrok authtoken <tu_token_aqui>
     ```

   - Solo necesitarás hacer esto una vez.

### 4. **Obtener el Enlace Público con Ngrok**
   - Ejecuta el siguiente comando para exponer el puerto 8000 a través de un enlace público:

     ```bash
     ngrok http 8000
     ```

   - Ngrok te proporcionará un enlace público (por ejemplo: `https://xxxx-xx-xx-xx.ngrok-free.app`) que podrás usar para acceder a tu API desde cualquier lugar.

---

## Conectar MongoDB

### 1. **Crear una Cuenta en MongoDB Atlas**
   - Dirígete a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) y crea una cuenta gratuita.
   - Una vez hayas creado tu cuenta, inicia sesión en el **Dashboard**.

### 2. **Crear un Cluster en MongoDB Atlas**
   - En el panel principal de MongoDB Atlas, haz clic en **Build a Cluster**.
   - Selecciona un plan gratuito y configura tu cluster (puedes elegir la región más cercana a tu ubicación).
   - Haz clic en **Create Cluster** y espera unos minutos hasta que se cree.

### 3. **Configurar el Acceso a la Base de Datos**
   - Una vez creado el cluster, necesitarás configurar el acceso a tu base de datos.
   - Dirígete a la sección **Database Access** y agrega un nuevo usuario con permisos de lectura y escritura.
     - Define un nombre de usuario y una contraseña.
   - Luego, dirígete a **Network Access** y agrega tu IP a la lista de direcciones IP permitidas.

### 4. **Obtener la URI de Conexión**
   - Ve a **Clusters** y haz clic en el botón **Connect** de tu cluster.
   - Selecciona la opción **Connect your application**.
   - Copia la URI de conexión que se te proporciona. Este URI será algo como:

     ```
     mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?retryWrites=true&w=majority
     ```

### 5. **Configurar el Archivo `.env`**
   - Crea un archivo `.env` en la raíz de tu proyecto si aún no lo tienes.
   - En el archivo `.env`, agrega la URI de conexión que copiaste en el paso anterior:

     ```env
     MONGO_URI=mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?retryWrites=true&w=majority
     ```

   - Asegúrate de reemplazar `<usuario>`, `<contraseña>`, y `<cluster>` con los valores correspondientes.

---

## Cargar los Datos de los Premios Oscar

Una vez configurada la base de datos y las variables de entorno, ejecuta el archivo `cargarPremiosOscar.py` para cargar los datos de los premios Oscar en la base de datos MongoDB.

Finalmente ejecuta el archivo cargarPremiosOscar y se subiran los datos a tu base de datos de Mongo Atlas.
