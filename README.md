# API PREMIOS OSCAR

## Pasos para configurar la API

1. **Registrarse en Ngrok**  
   Dirígete a [https://ngrok.com/](https://ngrok.com/) y regístrate para obtener una cuenta gratuita.

2. **Instalar Ngrok**  
   Descarga Ngrok desde [este enlace](https://download.ngrok.com/windows?tab=download) y sigue las instrucciones de instalación.

3. **Obtener tu token de Ngrok**  
   Después de registrarte, obtén tu token desde [aquí](https://dashboard.ngrok.com/get-started/your-authtoken).

4. **Configurar el archivo `main.py`**  
   Con el archivo `main.py` abierto en tu editor de Visual Studio, abre la terminal de Visual Studio y ejecuta el siguiente comando para desplegar la API:

   ```bash
   uvicorn main:app
Esto hará que la API se despliegue en localhost.

Configurar Ngrok en tu sistema

Pulsa Windows + R, escribe sysdm.cpl y presiona Enter.
Ve a Opciones avanzadas y luego a Variables de entorno.
En Variables de sistema, selecciona Path y haz clic en Editar.
Añade un nuevo path con la ruta donde se encuentre ngrok.exe en tu sistema.
Verificar la instalación de Ngrok
Abre la terminal o el CMD de Windows y ejecuta el siguiente comando para verificar que Ngrok está correctamente instalado:

bash
Copiar código
ngrok version
Esto debería mostrar la versión de Ngrok instalada.

Activar tu token de Ngrok
En el CMD de Windows, ejecuta el siguiente comando para activar tu token (reemplaza <tu_token_aqui> con tu token obtenido):

bash
Copiar código
ngrok authtoken <tu_token_aqui>
Una vez lo ejecutes, no necesitarás hacerlo nuevamente.

Obtener el enlace público con Ngrok
Ahora, ejecuta el siguiente comando para exponer el puerto 8000 a través de un enlace público:

bash
Copiar código
ngrok http 8000
Ngrok te proporcionará un enlace público (por ejemplo: https://xxxx-xx-xx-xx.ngrok-free.app), que podrás usar para acceder a tu API desde cualquier lugar.

Finalmente, ejecuta el archivo cargarPremiosOscar.py para cargar los datos de los premios Oscar en la base de datos.

