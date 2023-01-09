from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class RegisterUserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='user1', password='test_pass123')

    def test_register_valid_user(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'user_1',
            'email': 'user.1@example.com',
            'password1': 'test_pass123',
            'password2': 'test_pass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:success'))

    def test_register_invalid_password_length(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'user_1',
            'email': 'user.1@example.com',
            'password1': '123',
            'password2': '123',
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEquals(response.context['form'].errors['password2'], [
            'This password is too short. It must contain at least 8 characters.',
            'This password is too common.',
            'This password is entirely numeric.',
        ])

    def test_register_different_passwords(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'user_1',
            'email': 'user.1@example.com',
            'password1': 'test_pass123',
            'password2': 'test_pass456',
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEquals(response.context['form'].errors['password2'], ['The two password fields didn’t match.'])

    def test_register_invalid_email(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'user_1',
            'email': 'user.1com',
            'password1': 'test_pass123',
            'password2': 'test_pass123',
        })
        self.assertFalse(response.context['form'].is_valid())
        self.assertEquals(response.context['form'].errors['email'], ['Enter a valid email address.'])
