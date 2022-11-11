from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Entry


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Entry.objects.all()

    def lastmod(self, entry):
        return entry.pub_date

    def location(self, entry):
        return reverse(
            'blog:entry',
            kwargs={'category': entry.category.slug, 'slug': entry.slug}
        )
