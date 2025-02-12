import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    [
        (
            pytest.lazy_fixture('url_home'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_detail'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_login'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_signup'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_logout'),
            pytest.lazy_fixture('client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_edit'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_delete'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
        (
            pytest.lazy_fixture('url_edit'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            pytest.lazy_fixture('url_delete'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
    ]
)
def test_availability_pages(
    url,
    parametrized_client,
    expected_status,
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('url_edit'), pytest.lazy_fixture('url_delete'))
)
def test_redirects(client, url, url_login):
    expected_url = f'{url_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
