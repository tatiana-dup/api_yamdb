from django.core.validators import MaxValueValidator, RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from users.models import MdbUser
from .const import DEFAULT_VALUE, MAX_SCORE_VALUE, MIN_SCORE_VALUE


TEXT_LENGTH = 20


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
        return self.name[:TEXT_LENGTH]


class Category(BaseCategoryGenre):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenre):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.TextField('Описание', null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='titles'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        default=DEFAULT_VALUE,
        validators=(
            MaxValueValidator(MAX_SCORE_VALUE),
            MinValueValidator(MIN_SCORE_VALUE),
        ),
        error_messages={
            'validators': (
                f'Введите значение от {MAX_SCORE_VALUE}'
                f'до {MIN_SCORE_VALUE}.'
            )
        },
        verbose_name='Оценка',
    )
    author = models.ForeignKey(
        MdbUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='only one review',
            ),
        )

    def __str__(self):
        return self.text[:TEXT_LENGTH]


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        MdbUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_LENGTH]