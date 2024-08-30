<p align="center">
  <img width="150px" src="https://i.ibb.co/bXvzjXm/LOGO-h1.png" />
</p>

# PANEL-PARA-COLEGIOS


# WINDOWS

> [!CAUTION]
> Si es la primera vez que ejecutas el programa y no tienes mucha experiencia con django
> o en general con python puedes obtener algunos errores...
> <br>
> ### error al instalar paquetes
> si despues de ejecutar ```pip install -r requirements.txt```
> obtienes un error como:
> ```python
> error: subprocess-exited-with-error
> 
> × Getting requirements to build wheel did not run successfully.
> │ exit code: 1
> ╰─> See above for output.
> ```
> <br>
> Es un error de copilacion por no tener instaldo c++
> Puedes solucionarlo con este video:
> https://youtu.be/wTv8rNobJsw?si=6nO7UaryScIcNIo9


Ahora debes instalar este paquete antes de ejecutar el servidor:
<br>

```python manage.py tailwind install```


Si obtienes el siguiente error:
<br>

> [!CAUTION]
> CommandError: 
> It looks like node.js and/or npm is not installed or cannot be found.
> 
> Visit https://nodejs.org to download and install node.js for your system.
>
> If you have npm installed and still getting this error message, set NPM_BIN_PATH variable in settings.py to match path of NPM executable in your system.
>
> Example:
> NPM_BIN_PATH = "/usr/local/bin/npm"


Instala Nodejs con este link: 
<br>
[NodeJs](https://nodejs.org/en/download)

<br>
y vuelve a ejecutar

```python manage.py tailwind install```

> [!NOTE]
> Sigue los sigueintes pasos para ejecutar el programa:

crear entorno virtual:
```virtualenv env```

instalar requirements.txt:
```pip install -r requirements.txt```

usar manage:
```cd PANEL-PARA-COLEGIOS/colegio```

iniciar servidor:
```python manage.py runserver```

iniciar tailwind:
```python manage.py tailwind start```
> [!NOTE]
> Recuerda tener npm instalado


> [!CAUTION]
> Si estas manjando el codigo recuerda que estos cambios modificaran la base de datos, un error puede eliminar toda la informacion
> <br>

migrar: 
```python manage.py makemigrations users informacion administradores profesores gestores acudientes alumnos```

crear base de datos:
```python manage.py migrate```

crear usuario par pruebas:
```python manage.py createsuperuser ```

<hr>

RECUERDA QUE CADA CAMBIO DEBE SER DOCUMENTADO
Un buen codigo siempre debe tener una buena documentacion
en caso de errores recuerda agregarlos a las inusualidades del proyecto
</s>

# VISTAS:
## Login:

<img src="./Documentation/images/login.png">