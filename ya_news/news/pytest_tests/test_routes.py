import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, parametrized_client, expected_status',
    [
        ('home', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('detail', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('login', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('signup', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('logout', pytest.lazy_fixture('client'), HTTPStatus.OK),
        ('edit', pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        ('delete', pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (
            'edit',
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
        (
            'delete',
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ),
    ]
)
def test_availability_pages(
    name,
    parametrized_client,
    expected_status,
    all_urls
):
    url = all_urls[name]
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('edit', 'delete')
)
def test_redirects(client, all_urls, name):
    expected_url = f'{all_urls["login"]}?next={all_urls[name]}'
    response = client.get(all_urls[name])
    assertRedirects(response, expected_url)
