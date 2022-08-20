# coding: utf-8
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.test import TestCase

from .admin import UserAdmin, ProfileInline
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


class MyAdminTest(TestCase):

    def setUp(self):
        self.mail = 'test@example.com'
        self.location = 'Tlaxcala'
        self.slug = 'javier'
        self.user = User.objects.create_user(
            email=self.mail
        )
        self.user.is_superuser = True
        self.user.profile.location = self.location
        self.user.profile.slug = self.slug
        self.user.save()

        site = AdminSite()
        self.admin = UserAdmin(User, site)

        request_factory = RequestFactory()
        self.request = request_factory.get('/admin')
        self.request.user = self.user

        # If you need to test something using messages
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

    def test_profile_inline_class(self):
        self.assertEqual(ProfileInline.__name__, 'ProfileInline')

    def test_admin_inline_empty(self):
        self.assertTrue(isinstance(self.admin.get_inline_instances(self.request), list))

    def test_admin_inline(self):
        user_inline = self.admin.get_inline_instances(self.request, self.user)[0].__class__.__name__
        profile_inline = ProfileInline.__name__
        self.assertEqual(user_inline, profile_inline)

    def test_delete_model(self):
        self.admin.delete_model(self.request, self.user)
        deleted = User.objects.first()
        self.assertEqual(deleted, None)

    def test_save_model(self):
        self.admin.save_model(self.request, self.user, self.user, True)
        updated = User.objects.first()
        self.assertEqual(updated.email, self.mail)

    def test_save_formset(self):
        self.admin.save_formset(self.request, self.user, self.user, True)
        updated = User.objects.get(email=self.mail)
        self.assertEqual(updated.email, self.mail)

    def test_admin_location(self):
        self.assertEqual(self.admin.get_location(self.request.user), self.location)

    def test_admin_slug(self):
        self.assertEqual(self.admin.get_slug(self.request.user), self.slug)
