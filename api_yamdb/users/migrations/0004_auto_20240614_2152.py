# Generated by Django 3.2 on 2024-06-14 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_mdbuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdbuser',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
        migrations.AlterField(
            model_name='mdbuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Емейл'),
        ),
        migrations.AlterField(
            model_name='mdbuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='mdbuser',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', max_length=10, verbose_name='Роль'),
        ),
    ]