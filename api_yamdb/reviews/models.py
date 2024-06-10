from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


TEXT_LENGTH = 50


class BaseCategoryGenre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message=('Slug может содержать только буквы, '
                     'цифры, дефисы и подчеркивания.')
        )]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseCategoryGenre):
    ...


class Genre(BaseCategoryGenre):
    ...


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField('Slug жанра', Genre, through='GenreTitle')
    category = models.ForeignKey(
        'Slug категории', Category, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
