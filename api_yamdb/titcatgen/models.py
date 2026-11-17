from django.db import models

from .validators import max_value_this_year, min_value_first_year


class Category(models.Model):
    """Тип объекта: отель, гостевой дом или хостел."""
    name = models.CharField('Тип размещения', max_length=100)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тип размещения'
        verbose_name_plural = 'Типы размещения'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Особенность отдыха', max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Особенность отдыха'
        verbose_name_plural = 'Особенности отдыха'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Название объекта', max_length=200)
    year = models.PositiveSmallIntegerField(
        'Год открытия',
        validators=[
            max_value_this_year,
            min_value_first_year
        ],
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Тип размещения',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Особенности отдыха',
        related_name='titles',
        blank=True,
    )
    description = models.TextField('Описание объекта', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Объект размещения'
        verbose_name_plural = 'Объекты размещения'

    def __str__(self):
        return self.name
