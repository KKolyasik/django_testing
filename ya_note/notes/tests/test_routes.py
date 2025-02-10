from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username='testuser',
        )
        cls.guest = User.objects.create(
            username='guest',
        )
        cls.anonymous = User.objects.create(
            username='anonymous',
        )
        cls.notes = Note.objects.create(
            title='Test note',
            text='Test text',
            slug='test-note',
            author=cls.author
        )

    def test_pages_availability(self):
        urls = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(reverse(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authorised_user_pages_aviability(self):
        urls = (
            'notes:add',
            'notes:success',
            'notes:list',
        )
        self.client.force_login(self.author)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(reverse(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_detail_edit_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.guest, HTTPStatus.NOT_FOUND),
        )
        urls = (
            ('notes:detail', (self.notes.slug,)),
            ('notes:edit', (self.notes.slug,)),
            ('notes:delete', (self.notes.slug,)),
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for url, args in urls:
                with self.subTest(user=user, url=url):
                    response = self.client.get(reverse(url, args=args))
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.notes.slug,)),
            ('notes:delete', (self.notes.slug,)),
            ('notes:list', None),
            ('notes:detail', (self.notes.slug,)),
            ('notes:success', None),
        )
        for url, args in urls:
            with self.subTest(url=url):
                redirect_url = f'{login_url}?next={reverse(url, args=args)}'
                response = self.client.get(reverse(url, args=args))
                self.assertRedirects(response, redirect_url)
