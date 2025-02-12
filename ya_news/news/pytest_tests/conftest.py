import pytest
from django.test.client import Client
from news.models import News, Comment
from datetime import timedelta
from django.utils import timezone
from yanews import settings
from django.urls import reverse


@pytest.fixture(autouse=True)
def use_db(db):
    pass


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='not_author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Test news',
        text='Test text',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        text='Test comment',
        news=news,
        author=author,
    )
    return comment


@pytest.fixture
def all_urls(news, comment):
    return {
        'home': reverse('news:home'),
        'detail': reverse('news:detail', args=(news.pk,)),
        'delete': reverse('news:delete', args=(comment.pk,)),
        'edit': reverse('news:edit', args=(comment.pk,)),
        'login': reverse('users:login'),
        'logout': reverse('users:logout'),
        'signup': reverse('users:signup')
    }


@pytest.fixture
def many_news():
    all_news = [
        News(
            title=f'News {index}',
            text='Just text.',
            date=timezone.now() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def many_comments(news, author):
    for index in range(5):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Text {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data(news, author):
    return {
        'text': 'Test text',
        'news': news,
        'author': author
    }
