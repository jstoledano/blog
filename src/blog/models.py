# coding: utf-8

#         app: org.toledano.blog
#      module: blog.models
# description: Models for blog app
#      author: Javier Sanchez Toledano
#        date: 2022-08-25
#     licence: MIT
#      python: 3.10
import uuid
from datetime import datetime
from typing import List

import markdown
from django.conf import settings
from django.db import models
from django.template.defaultfilters import truncatechars_html, striptags, safe
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.utils.timezone import make_aware
import pytz
from django.conf import settings


MD_EXTENSIONS = [
    'markdown.extensions.codehilite',
    'markdown.extensions.meta',
    'markdown.extensions.abbr',
    'markdown.extensions.attr_list',
    'markdown.extensions.def_list',
    'markdown.extensions.fenced_code',
    'markdown.extensions.footnotes',
    'markdown.extensions.tables',
    'markdown.extensions.admonition',
    'markdown.extensions.sane_lists',
    'markdown.extensions.extra',
    'markdown.extensions.smarty',
    'markdown.extensions.toc',
]


class Traceability(models.Model):
    """
    An abstract class that serves as the basis for models.
    Automatically updates the ``created`` and ``modified`` fields.
    """
    idx = models.UUIDField(default=uuid.uuid4,  editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Traceability):
    name = models.CharField(
        _('Title'), max_length=255,
        help_text=_('Name of the category. Max length is 255.')
    )
    slug = models.SlugField(
        _('Slug'), max_length=60, unique=True,
        help_text=_('Slug of the category. Max length is 255.')
    )
    icon = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    description_html = models.TextField(editable=False, blank=True, null=True)

    class Meta:
        ordering = ['slug']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.description:
            self.description_html = markdown.markdown(
                self.description,
                output_format='html',
                extensions=MD_EXTENSIONS
            )
        super(Category, self).save(force_insert, force_update)

    def __str__(self) -> str:
        return self.name

    def permalink(self) -> str:
        return f'/category/{self.slug}'

    def get_absolute_url(self) -> str:
        return reverse('blog:category_detail', args=[self.slug])


class Entry(Traceability):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    # Main fields
    title = models.CharField(_('Title'), max_length=250)
    summary = models.TextField(_('Summary'), blank=True)
    body = models.TextField(_('Body'), blank=True)
    extend = models.TextField(_('Extend'), blank=True)
    pub_date = models.DateTimeField(default=datetime.now)

    # Fields to be filled with HTML output from Markdown
    summary_html = models.TextField(editable=False, blank=True)
    summary_meta = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)
    extend_html = models.TextField(editable=False, blank=True)

    # Metadata
    enable_comments = models.BooleanField(default=True)
    cover = models.URLField(blank=True)
    slug = models.SlugField(unique_for_date='pub_date')
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    featured = models.BooleanField(default=False)

    # Taxonomy
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='entry_category')
    tags = TaggableManager(blank=True)

    # Authoring metadata
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='entradas',
        editable=False,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Entradas'
        verbose_name = 'Entrada'
        ordering = ['-id', '-pub_date']
        unique_together = ('slug', 'category')
        get_latest_by = 'pub_date'

    def __str__(self) -> str:
        return self.title

    def save(self, force_insert=False, force_update=False, **kwargs) -> None:

        self.body_html = markdown.markdown(
            self.body,
            output_format='html',
            extensions=MD_EXTENSIONS
        )
        if self.summary:
            self.summary_html = markdown.markdown(
                self.summary,
                output_format='html',
                extensions=MD_EXTENSIONS
            )
            self.summary_meta = safe(striptags(self.summary_html))
        else:
            self.summary_html = safe(truncatechars_html(self.body_html, 250))
            self.summary_meta = striptags(self.summary_html)
        if self.extend:
            self.extend_html = markdown.markdown(
                self.extend,
                output_format='html',
                extensions=MD_EXTENSIONS
            )
        if not self.slug:
            self.slug = slugify(self.title)
        if self.pub_date.tzinfo is None or self.pub_date.tzinfo.utcoffset(self.pub_date) is None:
            self.pub_date = make_aware(self.pub_date, pytz.timezone('Mexico/General'))
        super(Entry, self).save(force_insert, force_update)

    def get_absolute_url(self) -> str:
        return reverse(
            'blog:entry_detail',
            kwargs={'category': self.category.slug, 'slug': self.slug}
        )

    def resumen(self):
        if self.summary:
            return safe(striptags(self.summary))
        else:
            return safe(striptags(truncatechars_html(self.body_html, 450)))

    def get_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append(str(tag))
        return tags