# Generated by Django 5.0.1 on 2024-03-27 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0008_rename_api_key_source_token_source_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='token',
            field=models.CharField(max_length=500),
        ),
    ]