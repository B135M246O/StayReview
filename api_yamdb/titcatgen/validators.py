from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator


def this_year():
    return datetime.now().year


def max_value_this_year(value):
    return MaxValueValidator(
        this_year(),
        'Год открытия не может быть в будущем.'
    )(value)


def min_value_first_year(value):
    return MinValueValidator(
        1,
        'Год открытия должен быть положительным.'
    )(value)
