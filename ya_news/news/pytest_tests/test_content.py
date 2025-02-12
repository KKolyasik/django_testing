import pytest
from news.forms import CommentForm
from yanews import settings


def test_news_count(client, many_news, url_home):
    response = client.get(url_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, many_news, url_home):
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(author_client, url_detail, many_comments):
    response = author_client.get(url_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'parametrzied_client, has_form',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_pages_contains_form(parametrzied_client, has_form, url_detail):
    response = parametrzied_client.get(url_detail)
    assert ('form' in response.context) == has_form


def test_comment_form_instance(author_client, url_detail):
    response = author_client.get(url_detail)
    assert 'form' in response.context
    form = response.context['form']
    assert isinstance(form, CommentForm)
