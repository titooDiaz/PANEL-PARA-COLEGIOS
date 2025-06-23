<p align="center">
  <img width="150px" src="https://i.ibb.co/bXvzjXm/LOGO-h1.png" alt="H1 Logo">
  <img width="150px" src="https://github.com/user-attachments/assets/e0551b39-11a1-4ce3-b5e2-2c6c18882bf0" alt="Project Logo">
</p>

# PANEL-PARA-COLEGIOS

This project is a school management system built with Django, designed to streamline academic and administrative operations within schools.

---

## Prerequisites

1. **Python**
   Ensure Python is installed (latest stable version recommended).

2. **Virtualenv**
   Used to isolate project dependencies:

   ```bash
   pip install virtualenv
   ```

3. **Node.js & npm**
   Tailwind CSS requires Node.js. Download it from the [official website](https://nodejs.org/en/download).

---

## Installation & Setup

### 1. Create a virtual environment

```bash
virtualenv env
```

### 2. Activate the virtual environment

```bash
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tailwind CSS

```bash
python manage.py tailwind install
```

#### Common Tailwind error

If you see:

```plaintext
CommandError:
It looks like node.js and/or npm is not installed or cannot be found.
```

Make sure Node.js and npm are installed and accessible. You may need to add your npm path to a `.env` file:

> If `.env` doesn’t exist yet, create it in the project root directory, next to folders like:

```
|- colegio/
|- Documentation/
|- mails templates/
|- requirements.txt
```

Inside `.env`, add:

```env
WHEREISNPM=/your/path/to/npm
INTERNAL_IPS=127.0.0.1
```

Find your npm path using:

```bash
whereis npm
```

you cant change the path in the `.env` file.

---

## Run the Project

### 1. Move to the Django app directory:

```bash
cd PANEL-PARA-COLEGIOS/colegio
```

### 2. Start the ASGI server (replaces `runserver`):

```bash
uvicorn core.asgi:application --host 127.0.0.1 --port 8000 --reload
```

> Note: Replace `127.0.0.1` and `8000` with your custom values if needed.
> <br>
> if you put your public ip in the `ALLOWED_HOSTS` in the `settings.py` file, you can use:
> <br>
> ```uvicorn core.asgi:application --host 0.0.0.0 --port 5000 --reload```

### 3. Run Tailwind in development mode:

```bash
python manage.py tailwind start
```

### 4. Install Uvicorn (Linux only)

```bash
pip install uvicorn
```

---

## Database & Migrations

### 1. Create migrations

```bash
python manage.py makemigrations users information admis teachers managers guardians students
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Create admin user

```bash
python manage.py createsuperuser
```

### 4. Collect Static Files
```bash
python manage.py collectstatic
```


> **Note:** Always document changes in models and migrations to prevent data loss.

---

## System Features

### Login View

<p align="center">
  <img src="./Documentation/images/login.png" alt="Login View">
</p>

### Panel View

<p align="center">
  <img src="./Documentation/images/about.png" alt="Panel View">
</p>

---

## Important Notes

* **Code & Database documentation:**
  Always document changes made to the codebase or DB.

* **Caution:**
  Editing migrations or making wrong changes can cause data loss.

---

**Thanks for contributing to the project!**
Clean code is always better with good documentation. 🚀
