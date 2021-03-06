# Generated by Django 3.2.13 on 2022-05-04 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='nome')),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', models.CharField(max_length=255, verbose_name='phone')),
                ('role', models.CharField(max_length=255, verbose_name='role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'collaborator',
                'verbose_name_plural': 'collaborators',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='core.collaborator', verbose_name='collaborator')),
            ],
            options={
                'verbose_name': 'evaluation',
                'verbose_name_plural': 'evaluations',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='full name')),
                ('birth_date', models.DateField(verbose_name='birth date')),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='phone')),
                ('cpf', models.CharField(blank=True, max_length=20, null=True, verbose_name='CPF')),
            ],
            options={
                'verbose_name': 'patient',
                'verbose_name_plural': 'patients',
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='unit name', max_length=100, verbose_name='nome')),
            ],
            options={
                'verbose_name': 'unit',
                'verbose_name_plural': 'units',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='service name', max_length=100, verbose_name='nome')),
                ('collaborators', models.ManyToManyField(blank=True, help_text='collaborators', related_name='services', to='core.Collaborator', verbose_name='collaborators')),
                ('unit', models.ForeignKey(help_text='unit', on_delete=django.db.models.deletion.CASCADE, to='core.unit', verbose_name='unit')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('prescription_date', models.DateField(verbose_name='prescription date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='core.collaborator', verbose_name='collaborator')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='core.patient', verbose_name='patient')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='core.service', verbose_name='prescription')),
            ],
            options={
                'verbose_name': 'prescription',
                'verbose_name_plural': 'prescriptions',
            },
        ),
        migrations.CreateModel(
            name='EvaluationAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='evaluations/attachments/')),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='core.evaluation', verbose_name='evaluation')),
            ],
            options={
                'verbose_name': 'evaluation attachment',
                'verbose_name_plural': 'evaluation attachments',
            },
        ),
        migrations.AddField(
            model_name='evaluation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='core.patient', verbose_name='patient'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='core.service', verbose_name='service'),
        ),
    ]
