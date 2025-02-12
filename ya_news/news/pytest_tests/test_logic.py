from pytest_django.asserts import assertRedirects
from news.models import Comment
from http import HTTPStatus


def test_user_can_create_comment(author_client, form_data, all_urls):
    response = author_client.post(all_urls['detail'], data=form_data)
    assertRedirects(response, all_urls['detail'] + '#comments')
    assert Comment.objects.count() == 2
    new_comment = Comment.objects.last()
    assert new_comment.text == form_data['text']
    assert new_comment.news == form_data['news']
    assert new_comment.author == form_data['author']


def test_other_users_cant_create_comment(client, form_data, all_urls):
    response = client.post(all_urls['detail'], data=form_data)
    expected_url = f'{all_urls["login"]}?next={all_urls["detail"]}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1


def test_user_can_edit_comment(author_client, comment, form_data, all_urls):
    response = author_client.post(all_urls['edit'], data=form_data)
    assertRedirects(response, all_urls['detail'] + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == form_data['author']
    assert comment.news == form_data['news']


def test_other_users_cant_edit_comment(
        not_author_client, form_data,
        comment,
        all_urls
):
    response = not_author_client.post(all_urls['edit'], data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author
    assert comment.news == comment_from_db.news


def test_user_can_delete_comment(author_client, all_urls, comment):
    response = author_client.delete(all_urls['delete'])
    url_redirect = all_urls['detail'] + '#comments'
    assertRedirects(response, url_redirect)
    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_other_users_cant_delete_comment(not_author_client, all_urls, comment):
    response = not_author_client.delete(all_urls['delete'])
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.pk).exists()
