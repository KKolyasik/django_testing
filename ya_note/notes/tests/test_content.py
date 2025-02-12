from .test_base import BaseTest
from notes.forms import NoteForm
from notes.models import Note


class TestNotesList(BaseTest):
    def test_note_in_list_for_author(self):
        response = self.auth_client.get(self.LIST_NOTES_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)
        note_db = Note.objects.get()
        self.assertEqual(
            (note_db.title, note_db.text, note_db.author, note_db.slug),
            (self.note.title, self.note.text, self.note.author, self.note.slug)
        )

    def test_note_not_in_list_for_guest(self):
        response = self.guest_client.get(self.LIST_NOTES_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_authorized_client_has_form(self):
        urls = (
            self.ADD_NOTE_URL,
            self.EDIT_URL
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
