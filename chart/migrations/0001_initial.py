# Generated by Django 5.0.1 on 2024-01-10 12:14

import chart.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('api_key', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='GlucoseValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=10)),
                ('time_of_reading', models.DateTimeField()),
                ('source', models.ForeignKey(default=chart.models.Source.get_default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, to='chart.source')),
            ],
        ),
    ]
