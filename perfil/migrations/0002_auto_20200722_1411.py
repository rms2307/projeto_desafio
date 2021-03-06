# Generated by Django 3.0.8 on 2020-07-22 17:11

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'Usuário só pode conter letras, digitos ou os seguintes caracteres: @ . + -', 'invalid')], verbose_name='Usuário'),
        ),
    ]
