from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class MdbUser(AbstractUser):
    email = models.EmailField('Емейл', unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    bio = models.TextField('Биография', blank=True)
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    role = models.CharField('Роль', max_length=10, choices=ROLE_CHOICES,
                            default=USER)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
