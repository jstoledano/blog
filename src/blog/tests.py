# coding: utf-8

#         app: org.toledano.blogApp
#      module: blog.test
# description: UnitTest for blog app
#      author: Javier Sanchez Toledano
#        date: 2022-08-21
#     licence: MIT
#      python: 3.10

from datetime import datetime

import factory
import pytz
from django.conf import settings
from django.test import TestCase
from django.utils.timezone import make_aware
from django.views.generic import TemplateView

from profiles.models import User
from .models import Category, Traceability, Entry
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from .admin import EntryAdmin, CategoryAdmin
from .views import IndexView


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')


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


class CategoryAdminTest(TestCase):
    def setUp(self):
        super().__init__()

        site = AdminSite()
        self.admin = CategoryAdmin(Category, site)
        request_factory = RequestFactory()
        self.request = request_factory.get('/admin')
        self.request.user = UserFactory(is_superuser=True)

    def test_category_admin_class(self):
        self.assertEqual(self.admin.__class__, CategoryAdmin)

    def test_category_full_admin_save(self):
        self.category_full = Category.objects.create(
            name='Web Development',
            slug='web-development', icon='fa fa-code',
            description='This is a **category**'
        )
        self.assertEqual(self.admin.save_model(self.request, self.category_full, None, None), None)

    def test_category_simple_admin_save(self):
        self.category_simple = Category.objects.create(
            name="Simple Category",
            slug="simple"
        )
        self.assertEqual(self.admin.save_model(self.request, self.category_simple, None, None), None)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'Test Category'
    slug = factory.Faker('slug')


class EntryTest(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        super().__init__()
        self.user = UserFactory()
        self.category = CategoryFactory(slug='otro-slug')
        self.full_entry = Entry.objects.create(
            title='Full Entry Creation',
            summary='This is a **full entry**',
            slug='full-entry-creation-2',
            body='_Hello_ **World**',
            extend='## This is a test',
            pub_date=make_aware(datetime(2022, 8, 21), pytz.timezone(settings.TIME_ZONE)),
            enable_comments=False,
            cover=factory.Faker('image_url'),
            status=Entry.LIVE_STATUS,
            featured=True,
            category=self.category,
            tags=['uno', 'dos', 'tres'],
            author=self.user
        )
        self.simple_entry = Entry.objects.create(
            title='Simple Entry Creation',
            body='''
Lorem ipsum dolor sit **amet**, consectetuer adipiscing elit. 
Aenean commodo _ligula eget dolor_. masa aeneana. Cum 
sociis natoque penatibus et **magnis** dis parturient montes, 
nascetur ridiculus mus. Donec quam felis, ultricies nec, 
pellentesque eu, pretium *quis, sem.*''',
            pub_date=make_aware(datetime(2022, 8, 21), pytz.timezone(settings.TIME_ZONE)),
            category=self.category,
            author=self.user
        )

    def test_entry_creation(self):
        self.assertEqual(self.full_entry.__class__, Entry)
        self.assertEqual(self.simple_entry.__class__, Entry)

    def test_entry_string(self):
        self.assertEqual(str(self.full_entry), 'Full Entry Creation')
        self.assertEqual(str(self.simple_entry), 'Simple Entry Creation')

    def test_entry_body_html(self):
        self.assertEqual(self.full_entry.body_html, '<p><em>Hello</em> <strong>World</strong></p>')

    def test_entry_short_summary_html(self):
        self.assertEqual(self.full_entry.summary_html, '<p>This is a <strong>full entry</strong></p>')

    def test_entry_short_summary(self):
        self.assertEqual(self.full_entry.summary_meta, 'This is a full entry')

    def test_entry_long_summary(self):
        summary_length = len(self.simple_entry.summary_meta)
        self.assertEqual(summary_length, 250)

    def test_full_entry_absolute_url(self):
        self.assertEqual(self.full_entry.get_absolute_url(), f'/{self.category.slug}/full-entry-creation-2')

    def test_simple_entry_absolute_url(self):
        self.assertEqual(self.simple_entry.get_absolute_url(), f'/{self.category.slug}/simple-entry-creation')

    def test_entry_tags(self):
        self.assertEqual(self.full_entry.tags, ['uno', 'dos', 'tres'])

    def test_entry_with_no_tags(self):
        self.assertEqual([tag.slug for tag in self.simple_entry.tags.all()], [])


class EntryAdminTest(TestCase):
    def setUp(self):
        super().__init__()
        self.author = UserFactory(is_superuser=True)
        self.category = CategoryFactory(slug='slug-admin')

        site = AdminSite()
        self.admin = EntryAdmin(Entry, site)
        request_factory = RequestFactory()
        self.request = request_factory.get('/admin')
        self.request.user = self.author

        self.entry = Entry.objects.create(
            title='Entry Admin Creation',
            slug='entry-admin-creation',
            body='_Hello_ **World**',
            category=self.category,
            author=self.author
        )

    def test_entry_admin_class(self):
        self.assertEqual(self.admin.__class__, EntryAdmin)

    def test_entry_admin_save(self):
        self.assertEqual(self.admin.save_model(self.request, self.entry, None, None), None)


class IndexPageText(TestCase):

    def test_index_view_instance(self):
        self.assertTrue(issubclass(IndexView, TemplateView))
