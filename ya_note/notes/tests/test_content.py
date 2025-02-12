from .test_base import BaseTest
from notes.forms import NoteForm


class TestNotesList(BaseTest):
    def test_notes_list(self):
        cases = (
            (self.auth_client, True),
            (self.guest_client, False)
        )
        for client, note_in_list in cases:
            with self.subTest():
                response = client.get(self.LIST_NOTES_URL)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), note_in_list)

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
