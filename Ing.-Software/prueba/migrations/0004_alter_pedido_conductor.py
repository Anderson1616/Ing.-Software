# Generated by Django 5.0.6 on 2024-07-01 19:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prueba', '0003_camion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='conductor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.conductor'),
        ),
    ]
