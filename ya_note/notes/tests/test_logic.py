from .test_base import BaseTest
from http import HTTPStatus
from notes.models import Note
from notes.forms import WARNING
from pytils.translit import slugify


class TestNotesCreate(BaseTest):
    def test_anonymous_user_cant_create_note(self):
        self.anonymous_client.post(self.ADD_NOTE_URL, self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_authorized_user_can_create_note(self):
        response = self.auth_client.post(self.ADD_NOTE_URL, self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)
        note = Note.objects.last()
        self.assertEqual(
            (note.title, note.text, note.slug),
            (
                self.form_data['title'],
                self.form_data['text'],
                self.form_data['slug']
            )
        )

    def test_unique_slug_for_note(self):
        self.form_data['slug'] = self.NOTE_SLUG
        response = self.auth_client.post(self.ADD_NOTE_URL, self.form_data)
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
        response = self.auth_client.post(self.ADD_NOTE_URL, self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 2)
        new_note_slug = Note.objects.last().slug
        expected_slug = slugify(self.form_data['title'])[:100]
        self.assertEqual(new_note_slug, expected_slug)


class TestNotesEditDelete(BaseTest):
    def test_author_can_delete_note(self):
        response = self.auth_client.post(self.DELETE_URL)
        self.assertRedirects(response, self.SUCCESS_URL)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_guest_cant_delete_note(self):
        response = self.guest_client.post(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_author_can_edit_note(self):
        response = self.auth_client.post(self.EDIT_URL, self.form_data)
        self.assertRedirects(response, self.SUCCESS_URL)
        self.note.refresh_from_db()
        self.assertEqual(
            (self.note.title, self.note.text, self.note.slug),
            (
                self.form_data['title'],
                self.form_data['text'],
                self.form_data['slug']
            )
        )
