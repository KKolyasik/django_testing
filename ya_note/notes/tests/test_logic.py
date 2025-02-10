from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note
from notes.forms import WARNING
from pytils.translit import slugify

User = get_user_model()


class TestNotesCreate(TestCase):

    NOTE_TEXT = 'Test text'
    NOTE_TITLE = 'Test title'
    NOTE_SLUG = 'test-slug'

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add')
        cls.succes_url = reverse('notes:success')
        cls.author = User.objects.create(
            username='testuser'
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG
        }

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_authorized_user_can_create_note(self):
        response = self.author_client.post(self.url, self.form_data)
        self.assertRedirects(response, self.succes_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(
            (note.title, note.text, note.author, note.slug),
            (self.NOTE_TITLE, self.NOTE_TEXT, self.author, self.NOTE_SLUG)
        )

    def test_unique_slug_for_note(self):
        self.author_client.post(self.url, self.form_data)
        response = self.author_client.post(self.url, {
            'title': 'Another title',
            'text': 'Another text',
            'slug': self.NOTE_SLUG
        })
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.NOTE_SLUG + WARNING
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        response = self.author_client.post(self.url, self.form_data)
        self.assertRedirects(response, self.succes_url)
        self.assertEqual(Note.objects.count(), 1)
        new_note_slug = Note.objects.get().slug
        expected_slug = slugify(self.form_data['title'])[:100]
        self.assertEqual(new_note_slug, expected_slug)


class TestNotesEditDelete(TestCase):

    NOTE_TEXT = 'Test text'
    NOTE_TITLE = 'Test title'
    NOTE_SLUG = 'test-slug'
    NEW_NOTE_TEXT = 'Another text'
    NEW_NOTE_TITLE = 'Another title'
    NEW_NOTE_SLUG = 'another-slug'

    @classmethod
    def setUpTestData(cls):
        cls.url_success = reverse('notes:success')
        cls.author = User.objects.create(
            username='testuser'
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.guest = User.objects.create(
            username='guest'
        )
        cls.guest_client = Client()
        cls.guest_client.force_login(cls.guest)
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author
        )
        cls.url_edit = reverse('notes:edit', args=(cls.NOTE_SLUG,))
        cls.url_delete = reverse('notes:delete', args=(cls.NOTE_SLUG,))
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.NEW_NOTE_SLUG
        }

    def test_author_can_delete_note(self):
        response = self.author_client.post(self.url_delete)
        self.assertRedirects(response, self.url_success)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_guest_cant_delete_note(self):
        response = self.guest_client.post(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.url_edit, self.form_data)
        self.assertRedirects(response, self.url_success)
        self.note.refresh_from_db()
        self.assertEqual(
            (self.note.title, self.note.text, self.note.slug),
            (self.NEW_NOTE_TITLE, self.NEW_NOTE_TEXT, self.NEW_NOTE_SLUG)
        )

    def test_guest_cant_edit_note(self):
        response = self.guest_client.post(self.url_edit, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(
            (self.note.title, self.note.text, self.note.slug),
            (self.NOTE_TITLE, self.NOTE_TEXT, self.NOTE_SLUG)
        )
