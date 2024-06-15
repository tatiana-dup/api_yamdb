from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username
from users.constants import FIRST_NAME_MAX_LENGTH, USERNAME_MAX_LENGTH


class MdbUser(AbstractUser):

    class UserRoles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField('Емейл', unique=True)
    username = models.CharField(
        'Юзернейм',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username],
        error_messages={
            'unique': 'Пользователь с таким юзернеймом уже существует.',
        },
    )
    first_name = models.CharField(
        'Имя',
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=max([len(choice[0]) for choice in UserRoles.choices]),
        choices=UserRoles.choices,
        default=UserRoles.USER)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        return (self.role == self.UserRoles.ADMIN
                or self.is_staff
                or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MODERATOR
