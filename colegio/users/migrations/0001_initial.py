# Generated by Django 4.2.4 on 2023-09-03 21:54

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('informacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserAlumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('foto', models.ImageField(blank=True, default='alumnos/profile.png', null=True, upload_to=users.models.user_directory_path_profile)),
                ('tipo_documento', models.CharField(choices=[('Sin Informacion', 'Sin Informacion'), ('Tarjeta de Identidad', 'Tarjeta de Identidad'), ('Cédula de Ciudadanía', 'Cédula de Ciudadanía'), ('Cédula de Extranjería', 'Cédula de Extranjería'), ('Registro Civil de Nacimiento', 'Registro Civil de Nacimiento'), ('Permiso Especial de Permanencia', 'Permiso Especial de Permanencia')], default='Sin informacion', max_length=50)),
                ('descripcion', models.TextField()),
                ('introduccion', models.TextField()),
                ('numero_documento', models.CharField(blank=True, max_length=20, null=True)),
                ('tipo_usuario', models.CharField(choices=[('Profesor', 'Profesor'), ('Alumno', 'Alumno'), ('Gestor', 'Gestor'), ('Administrador', 'Administrador')], default='Alumno', max_length=50)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('sexo', models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('Sin informacion', 'Sin informacion')], default='Sin informacion', max_length=20)),
                ('estado', models.BooleanField(default=True)),
                ('alergias', models.TextField(blank=True, null=True)),
                ('condiciones_medicas', models.TextField(blank=True, null=True)),
                ('medicamentos_actuales', models.TextField(blank=True, null=True)),
                ('grupo_sanguineo', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'), ('Desconocido', 'Desconocido')], default='Desconocido', max_length=15, null=True)),
                ('contacto_emergencia_nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('contacto_emergencia_telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('ver_notas', models.BooleanField(default=True)),
                ('grado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='informacion.grado')),
                ('groups', models.ManyToManyField(blank=True, related_name='profesor_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='profesor_user_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
