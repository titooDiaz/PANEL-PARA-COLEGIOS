# PANEL-PARA-COLEGIOS
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
