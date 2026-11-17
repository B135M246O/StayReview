from django.db import models
from titcatgen.models import Title
from users.models import User

from .validators import validate_score

SCORE = [(i, i) for i in range(1, 11)]


class Review(models.Model):
    score = models.IntegerField(
        'Оценка проживания',
        choices=SCORE,
        blank=False,
        null=False,
        validators=[
            validate_score,
        ]
    )
    title = models.ForeignKey(
        to=Title,
        verbose_name='Объект размещения',
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('score',)
        verbose_name = 'Отзыв о проживании'
        verbose_name_plural = 'Отзывы о проживании'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='uniq_author',
            ),
        )

    def __str__(self):
        return f'{self.author} - {self.text[:15]}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('text', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} - {self.text[:15]}'
