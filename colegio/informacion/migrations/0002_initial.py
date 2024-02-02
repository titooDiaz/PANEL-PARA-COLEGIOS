# Generated by Django 4.2.4 on 2024-02-02 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('informacion', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='materias',
            name='alumnos1',
            field=models.ManyToManyField(blank=True, related_name='alumnos_electiva1', to='users.customuseralumno'),
        ),
        migrations.AddField(
            model_name='materias',
            name='alumnos2',
            field=models.ManyToManyField(blank=True, related_name='alumnos_electiva2', to='users.customuseralumno'),
        ),
        migrations.AddField(
            model_name='materias',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador_materia', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='materias',
            name='profe1',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='profesor_0', to='users.customuserprofesores'),
        ),
        migrations.AddField(
            model_name='materias',
            name='profe2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profesor_1', to='users.customuserprofesores'),
        ),
        migrations.AddField(
            model_name='horarios_partes',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador_de_materia', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='horariodiario',
            name='grado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='informacion.grado'),
        ),
        migrations.AddField(
            model_name='horariodiario',
            name='jueves',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materias_grado_4', to='informacion.materias'),
        ),
        migrations.AddField(
            model_name='horariodiario',
            name='lunes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materias_grado_1', to='informacion.materias'),
        ),
        migrations.AddField(
            model_name='horariodiario',
            name='martes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materias_grado_2', to='informacion.materias'),
        ),
        migrations.AddField(
            model_name='horariodiario',
            name='miercoles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materias_grado_3', to='informacion.materias'),
        ),
        migrations.AddField(
            model_name='horariodiario',
            name='viernes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materias_grado_5', to='informacion.materias'),
        ),
        migrations.AddField(
            model_name='grado',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador_grado', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='grado',
            name='horario_partes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='informacion.horarios_partes'),
        ),
        migrations.AddField(
            model_name='grado',
            name='materias',
            field=models.ManyToManyField(blank=True, related_name='materias_grado', to='informacion.materias'),
        ),
        migrations.AddField(
            model_name='colegio',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creador_colegio', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GradoProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Grados Escolares',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('informacion.grado',),
        ),
        migrations.CreateModel(
            name='HorarioDiarioProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Horarios Escolares',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('informacion.horariodiario',),
        ),
        migrations.CreateModel(
            name='Horarios_PartesProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Fraccion de horarios',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('informacion.horarios_partes',),
        ),
        migrations.CreateModel(
            name='MateriasProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Materias Escolares',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('informacion.materias',),
        ),
    ]
