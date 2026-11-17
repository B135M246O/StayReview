from datetime import date

import pytest
from django.core import mail
from django.core.management import call_command
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from reviews.models import Comment, Review
from reviews.validators import validate_score
from titcatgen.models import Category, Genre, Title
from users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def catalog():
    category = Category.objects.create(name='Гостевой дом', slug='guest-house')
    feature = Genre.objects.create(name='Для семьи', slug='family')
    stay = Title.objects.create(name='Лесной двор', year=2019, category=category)
    stay.genre.add(feature)
    return stay


@pytest.fixture
def client():
    return APIClient()


def test_signup_confirmation_and_jwt(client):
    response = client.post('/api/v1/auth/signup/', {
        'username': 'traveller', 'email': 'traveller@example.org',
    })
    assert response.status_code == 200
    user = User.objects.get(username='traveller')
    assert len(mail.outbox) == 1
    assert user.confirmation_code in mail.outbox[0].body
    assert user.confirmation_code != 'XXXX'
    token = client.post('/api/v1/auth/token/', {
        'username': user.username, 'confirmation_code': user.confirmation_code,
    })
    assert token.status_code == 201
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.data['token']}")
    assert client.get('/api/v1/users/me/').data['username'] == 'traveller'
    assert client.patch('/api/v1/users/me/', {'role': 'admin'}).data['role'] == 'user'


def test_confirmation_codes_are_individual():
    one = User.objects.create_user(username='one', email='one@example.org')
    two = User.objects.create_user(username='two', email='two@example.org')
    assert one.confirmation_code != two.confirmation_code


def test_catalog_filter_and_admin_create(client, catalog):
    result = client.get('/api/v1/titles/?category=guest-house&genre=family')
    assert result.status_code == 200
    assert result.data['results'][0]['name'] == 'Лесной двор'
    data = {'name': 'Маяк', 'year': 2020, 'category': 'guest-house', 'genre': ['family']}
    assert client.post('/api/v1/titles/', data).status_code == 401
    admin = User.objects.create_superuser(username='admin', email='admin@example.org', password='local-test-pass')
    client.force_authenticate(admin)
    assert client.post('/api/v1/titles/', data).status_code == 201
    data['year'] = date.today().year + 1
    assert client.post('/api/v1/titles/', data).status_code == 400


def test_reviews_rating_comments_and_permissions(client, catalog):
    author = User.objects.create_user(username='author', email='author@example.org')
    other = User.objects.create_user(username='other', email='other@example.org')
    moderator = User.objects.create_user(username='moderator', email='moderator@example.org', role='moderator')
    url = f'/api/v1/titles/{catalog.pk}/reviews/'
    assert client.post(url, {'score': 8, 'text': 'Тихие комнаты'}).status_code == 401
    client.force_authenticate(author)
    review = client.post(url, {'score': 8, 'text': 'Тихие комнаты'})
    assert review.status_code == 201
    assert client.post(url, {'score': 9, 'text': 'Второй отзыв'}).status_code == 400
    assert client.get(f'/api/v1/titles/{catalog.pk}/').data['rating'] == 8
    detail = f"{url}{review.data['id']}/"
    client.force_authenticate(other)
    assert client.patch(detail, {'text': 'Чужое изменение'}).status_code == 403
    comments_url = f'{detail}comments/'
    comment = client.post(comments_url, {'text': 'Спасибо за отзыв'})
    assert comment.status_code == 201
    assert Comment.objects.get(pk=comment.data['id']).author == other
    client.force_authenticate(moderator)
    assert client.delete(f"{comments_url}{comment.data['id']}/").status_code == 204
    assert client.delete(detail).status_code == 204
    assert not Review.objects.exists()


@pytest.mark.parametrize('score', [0, 11, -1])
def test_score_range_enforced_by_api_and_model(client, catalog, score):
    user = User.objects.create_user(username='author', email='author@example.org')
    client.force_authenticate(user)
    assert client.post(f'/api/v1/titles/{catalog.pk}/reviews/', {'score': score, 'text': 'Отзыв'}).status_code == 400
    with pytest.raises(ValidationError):
        validate_score(score)


def test_comment_cannot_be_read_through_another_stay(client, catalog):
    author = User.objects.create_user(username='author', email='author@example.org')
    review = Review.objects.create(title=catalog, author=author, score=8, text='Уютно')
    another = Title.objects.create(name='Другой объект', year=2020)
    url = f'/api/v1/titles/{another.pk}/reviews/{review.pk}/comments/'
    assert client.get(url).status_code == 404
    client.force_authenticate(author)
    assert client.post(url, {'text': 'Комментарий'}).status_code == 404


def test_demo_fixture_loads_domain_records_without_accounts():
    call_command('loaddata', 'fixtures.json', verbosity=0)
    assert Category.objects.count() == 3
    assert Genre.objects.count() == 3
    assert Title.objects.count() == 3
    assert not User.objects.exists()
