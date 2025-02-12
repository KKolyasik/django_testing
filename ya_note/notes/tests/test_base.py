from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()


class BaseTest(TestCase):
    # Константы
    TEST_USERNAME = "testuser"
    GUEST_USERNAME = "guest"
    NOTE_SLUG = "test-note"
    NOTE_TITLE = "Test title"
    NOTE_TEXT = "Test text"

    # Постоянные URL
    HOME_URL = reverse("notes:home")
    LOGIN_URL = reverse("users:login")
    LOGOUT_URL = reverse("users:logout")
    SIGNUP_URL = reverse("users:signup")
    ADD_NOTE_URL = reverse('notes:add')
    LIST_NOTES_URL = reverse('notes:list')
    SUCCESS_URL = reverse('notes:success')

    @classmethod
    def detail_url(cls, slug):
        return reverse("notes:detail", args=(slug,))

    @classmethod
    def edit_url(cls, slug):
        return reverse("notes:edit", args=(slug,))

    @classmethod
    def delete_url(cls, slug):
        return reverse("notes:delete", args=(slug,))

    @classmethod
    def setUpTestData(cls):
        # Создаем пользователей
        cls.user = User.objects.create_user(
            username=cls.TEST_USERNAME, password="testpassword"
        )
        cls.guest = User.objects.create_user(
            username=cls.GUEST_USERNAME, password="guestpassword"
        )

        # Заметка
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.user
        )

        # Динамические URL, зависящие от созданных данных
        cls.DETAIL_URL = cls.detail_url(cls.note.slug)
        cls.EDIT_URL = cls.edit_url(cls.note.slug)
        cls.DELETE_URL = cls.delete_url(cls.note.slug)

        # Клиенты:
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

        cls.guest_client = Client()
        cls.guest_client.force_login(cls.guest)

        cls.anonymous_client = Client()

        # Форма
        cls.form_data = {
            'text': cls.NOTE_TEXT,
            'title': cls.NOTE_TITLE,
            'slug': 'another-test-note'
        }
