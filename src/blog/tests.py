from datetime import datetime

import factory
import pytz
from django.conf import settings
from django.test import TestCase
from django.utils.timezone import make_aware

from profiles.models import User
from .models import Category, Traceability, Entry


class CategoryTest(TestCase):
    def setUp(self):
        super().__init__()
        self.category_full = Category.objects.create(
            name='Web Development',
            slug='web-development', icon='fa fa-code',
            description='This is a **category**'
        )
        self.category_simple = Category.objects.create(
            name="Simple Category",
            slug="simple"
        )

    def test_category_traceability_inheritance(self):
        self.assertTrue(issubclass(self.category_full.__class__, Traceability))
        self.assertTrue(issubclass(self.category_simple.__class__, Traceability))

    def test_category_creation(self):
        self.assertEqual(self.category_full.__class__, Category)
        self.assertEqual(self.category_simple.__class__, Category)

    def test_category_creation_with_name(self):
        self.assertEqual(self.category_full.name, 'Web Development')
        self.assertEqual(self.category_simple.name, 'Simple Category')

    def test_category_string(self):
        self.assertEqual(str(self.category_full), 'Web Development')
        self.assertEqual(str(self.category_simple), 'Simple Category')

    def test_category_slug_field(self):
        self.assertEqual(self.category_full.slug, 'web-development')
        self.assertEqual(self.category_simple.slug, 'simple')

    def test_category_icon_field(self):
        self.assertEqual(self.category_full.icon, 'fa fa-code')
        self.assertEqual(self.category_simple.icon, None)

    def test_category_description_field(self):
        self.assertEqual(self.category_full.description, 'This is a **category**')
        self.assertEqual(self.category_simple.description, None)

    def test_category_description_html_field(self):
        self.assertEqual(self.category_full.description_html, '<p>This is a <strong>category</strong></p>')
        self.assertEqual(self.category_simple.description_html, None)

    def test_category_permalink(self):
        self.assertEqual(self.category_full.permalink(), '/category/web-development')
        self.assertEqual(self.category_simple.permalink(), '/category/simple')

    def test_category_absolute_url(self):
        self.assertEqual(self.category_full.get_absolute_url(), '/category/web-development')
        self.assertEqual(self.category_simple.get_absolute_url(), '/category/simple')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'Test Category'
    slug = factory.Faker('slug')


class EntryTest(TestCase):
    def setUp(self) -> None:
        super().__init__()
        self.user = UserFactory()
        self.category = CategoryFactory(slug='otro-slug')
        self.full_entry = Entry.objects.create(
            title='Full entry Creation',
            summary='This is a **full** entry',
            slug='full-entry-creation-2',
            body='_Hello_ **World**',
            extend='## This is a test',
            pub_date=make_aware(datetime(2022, 8, 21), pytz.timezone(settings.TIME_ZONE)),
            enable_comments=False,
            cover=factory.Faker('image_url'),
            status=Entry.LIVE_STATUS,
            featured=True,
            category=self.category,
            tags=[],
            author=self.user
        )
        self.simple_entry = Entry.objects.create(
            title='Simple entry Creation',
            body='_Hello_ **World**',
            pub_date=make_aware(datetime(2022, 8, 21), pytz.timezone(settings.TIME_ZONE)),
            category=self.category,
            author=self.user
        )

    def test_entry_creation(self):
        self.assertEqual(self.full_entry.__class__, Entry)
        self.assertEqual(self.simple_entry.__class__, Entry)
