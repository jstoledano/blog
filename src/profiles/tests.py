from django.test import TestCase
from profile.models import Profile


class ProfileTest(TestCase):
    def setUp(self):
        pass

    def test_profile_creation(self):
        user = Profile.objects.create_user(
            username='test',
        )
        self.assertTrue(isinstance(user, Profile))