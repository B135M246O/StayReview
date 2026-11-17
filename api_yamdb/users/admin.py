from django.contrib import admin
from reviews.models import Comment, Review
from titcatgen.models import Category, Genre, Title

from .models import User

admin.site.site_header = 'StayReview — управление каталогом'
admin.site.site_title = 'StayReview'
admin.site.index_title = 'Объекты, отзывы и пользователи'

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
