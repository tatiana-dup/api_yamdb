# Generated by Django 3.2 on 2024-06-13 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mdbuser',
            options={'ordering': ['id']},
        ),
    ]
