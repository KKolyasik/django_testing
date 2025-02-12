from .test_base import BaseTest
from http import HTTPStatus


class TestRoutes(BaseTest):
    def test_pages_availability(self):
        cases = [
            [self.HOME_URL, self.anonymous_client, HTTPStatus.OK],
            [self.LOGIN_URL, self.anonymous_client, HTTPStatus.OK],
            [self.LOGOUT_URL, self.anonymous_client, HTTPStatus.OK],
            [self.SIGNUP_URL, self.anonymous_client, HTTPStatus.OK],
            [self.ADD_NOTE_URL, self.auth_client, HTTPStatus.OK],
            [self.SUCCESS_URL, self.auth_client, HTTPStatus.OK],
            [self.LIST_NOTES_URL, self.auth_client, HTTPStatus.OK],
            [self.EDIT_URL, self.auth_client, HTTPStatus.OK],
            [self.DELETE_URL, self.auth_client, HTTPStatus.OK],
            [self.DETAIL_URL, self.auth_client, HTTPStatus.OK],
            [self.EDIT_URL, self.guest_client, HTTPStatus.NOT_FOUND],
            [self.DELETE_URL, self.guest_client, HTTPStatus.NOT_FOUND],
            [self.DETAIL_URL, self.guest_client, HTTPStatus.NOT_FOUND],
        ]
        for url, client, status in cases:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect(self):
        urls = (
            self.ADD_NOTE_URL,
            self.EDIT_URL,
            self.DELETE_URL,
            self.DETAIL_URL,
            self.LIST_NOTES_URL,
            self.SUCCESS_URL
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.LOGIN_URL}?next={url}'
                response = self.anonymous_client.get(url)
                self.assertRedirects(response, redirect_url)
