from django.test import TestCase

from .models import Category, Traceability


class CategoryTest(TestCase):
    def setUp(self):
        super().__init__()
        self.category = Category.objects.create(
            name='Web Development',
            slug='web-development',
            icon='fa fa-code',
            description='Web _Development_ category'
        )
        self.category.save()

    def test_category_traceability_inheritance(self):
        self.assertTrue(issubclass(self.category.__class__, Traceability))

    def test_category_creation(self):
        self.assertEqual(self.category.__class__.__name__, 'Category')

    def test_category_creation_with_name(self):
        self.assertEqual(self.category.name, 'Web Development')

    def test_category_string(self):
        self.assertEqual(str(self.category), 'Web Development')

    def test_category_slug_field(self):
        self.assertEqual(self.category.slug, 'web-development')

    def test_category_icon_field(self):
        self.assertEqual(self.category.icon, 'fa fa-code')

    def test_category_description_field(self):
        self.assertEqual(self.category.description, 'Web _Development_ category')

    def test_category_description_html_field(self):
        self.assertEqual(self.category.description_html, '<p>Web <em>Development</em> category</p>')

    def test_category_permalink(self):
        self.assertEqual(self.category.permalink(), '/category/web-development')

    def test_category_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), '/category/web-development')
