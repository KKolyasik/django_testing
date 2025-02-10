from django.urls import reverse
from pytest_django.asserts import assertRedirects
from news.models import Comment
from http import HTTPStatus


def test_user_can_create_comment(author_client, author, form_data, news):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, url + '#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_other_users_cant_create_comment(client, form_data, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_can_edit_comment(author_client, news, form_data, comment):
    url = reverse('news:edit', args=(comment.pk,))
    response = author_client.post(url, data=form_data)
    url_redirect = reverse('news:detail', args=(news.pk,)) + '#comments'
    assertRedirects(response, url_redirect)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_users_cant_edit_comment(not_author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.pk,))
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment.text == comment_from_db.text


def test_user_can_delete_comment(author_client, comment, news):
    url = reverse('news:delete', args=(comment.pk,))
    response = author_client.delete(url)
    url_redirect = reverse('news:detail', args=(news.pk,)) + '#comments'
    assertRedirects(response, url_redirect)
    assert Comment.objects.count() == 0


def test_other_users_cant_delete_comment(not_author_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
