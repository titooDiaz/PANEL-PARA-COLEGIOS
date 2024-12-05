
---

# Aplicación de Gestión Escolar

## Descripción General

La aplicación tiene como temática principal una paleta de colores **rojo**, **naranja** y **amarillo**, representando energía, creatividad y enfoque. Este proyecto busca ofrecer una solución integral para la administración escolar, desde usuarios básicos hasta gestores y administradores.

---

## Historial de Desarrollo

### 26/08/2023
1. **Paleta de Colores:**  
   La temática de colores seleccionada refuerza el dinamismo y creatividad del entorno educativo.

2. **Configuración Inicial:**  
   Se configuraron los requerimientos base e integración con Tailwind CSS.  
   Fragmento relevante de `settings.py`:
   ```python
   # Configuración de idiomas
   LANGUAGES = [
       ('en', _('English')),
       ('es', _('Spanish')),
   ]

   LANGUAGE_CODE = 'es'  # Idioma por defecto: Español

   DEBUG = True
   ALLOWED_HOSTS = []

   # Aplicaciones instaladas
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       # Bibliotecas instaladas
       'tailwind',  # python manage.py tailwind init
       'theme',  # python manage.py tailwind install
       # Aplicaciones locales
       'users',
   ]

   # Integración con Node.js
   NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
   ```
3. **Estructura Base de Usuarios:**  
   - **Vista principal (`core`):** Punto inicial para las modificaciones constantes del diseño.

---

### 31/08/2023
**Creación y Gestión de Usuarios:**  
El sistema incluye diferentes tipos de usuarios según el nivel de acceso:  
1. **Usuarios básicos (`users`):**  
   Estudiantes registrados en la plataforma.  
2. **Profesores (`teachers`):**  
   Docentes encargados de crear y evaluar actividades.  
3. **Gestores (`managers`):**  
   Usuarios con permisos para visualizar toda la información, como coordinadores académicos o psicólogos.  
4. **Administradores (`admins`):**  
   Acceso completo para personalizar la plataforma, gestionar usuarios, cursos, y más.

---

### 11/04/2024
**Expansión del Proyecto:**  
Se decidió escalar la aplicación para soportar múltiples colegios en un solo servidor, con el objetivo de **abaratar costos**.  
- Cada colegio tendrá un **usuario gestor** inicial, quien podrá:
  - Crear usuarios adicionales.
  - Administrar el contenido de su institución.  
- Se evaluará la posibilidad de agregar **costos por número de usuarios**.

---

### 13/11/2024
**Nuevas Funcionalidades:**  
- Los estudiantes ya pueden subir actividades asignadas por los profesores.  
- El código base será reescrito en **inglés** para facilitar futuras integraciones y colaboraciones internacionales.

---

## Tecnologías Utilizadas

- **Backend:** Django  
- **Frontend:** Tailwind CSS  
- **Base de Datos:** PostgreSQL  
- **Otros:** Node.js, Django-Humanize  

---

## Próximos Pasos
1. Optimizar el diseño responsivo para dispositivos móviles.  
2. Implementar planes de suscripción basados en el número de usuarios por colegio.  
3. Integrar notificaciones en tiempo real.  

---