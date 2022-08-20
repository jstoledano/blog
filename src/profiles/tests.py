from django.test import TestCase
from .models import User, Profile


class UserTest(TestCase):
    def setUp(self):
        self.mail = 'test@example.com'
        self.user = User.objects.create_user(
            email=self.mail
        )
        self.user.save()
        self.profile = Profile.objects.get(user=self.user)

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))

    def test_user_string(self):
        self.assertEqual(self.user.__str__(), self.mail)

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_profile_string(self):
        self.assertEqual(self.profile.__str__(), self.mail)

