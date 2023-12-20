# PANEL-PARA-COLEGIOS


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


python manage.py tailwind install
CommandError: 
It looks like node.js and/or npm is not installed or cannot be found.

Visit https://nodejs.org to download and install node.js for your system.

If you have npm installed and still getting this error message, set NPM_BIN_PATH variable in settings.py to match path of NPM executable in your system.

Example:
NPM_BIN_PATH = "/usr/local/bin/npm"

https://nodejs.org/en/download

crear entorno virtual:
virtualenv env

instalar requirements.txt:
pip install -r requirements.txt

usar manage:
cd PANEL-PARA-COLEGIOS/colegio

iniciar servidor:
python manage.py runserver

iniciar tailwind:
python manage.py tailwind start

migrar: 
python manage.py makemigrations users informacion administradores profesores gestores acudientes alumnos

crear base de datos:
python manage.py migrate

crear usuario par pruebas:
python manage.py createsuperuser 
