# Generated by Django 4.2.4 on 2023-09-03 21:58

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuseralumno',
            name='foto',
            field=models.ImageField(blank=True, default='alumnos/profile.png', null=True, upload_to=users.models.user_directory_path_profile),
        ),
    ]