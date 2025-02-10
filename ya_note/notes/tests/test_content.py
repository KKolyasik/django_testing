from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model
from notes.forms import NoteForm


User = get_user_model()


class TestNotesList(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.list_url = reverse('notes:list')
        cls.author = User.objects.create(
            username='testuser'
        )
        cls.guest = User.objects.create(
            username='guest'
        )
        cls.note = Note.objects.create(
            title='Test note',
            text='Test text',
            author=cls.author
        )

    def test_notes_list(self):
        users = (
            (self.author, True),
            (self.guest, False)
        )
        for user, note_in_list in users:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(self.list_url)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), note_in_list)

    def test_authorized_cliend_has_form(self):
        self.client.force_login(self.author)
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for url, args in urls:
            with self.subTest(url=url):
                response = self.client.get(reverse(url, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
