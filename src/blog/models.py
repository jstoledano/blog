import uuid

import markdown
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.conf import settings

from taggit.managers import TaggableManager

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
    tags = TaggableManager()

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

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, **kwargs):

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
        if self.extend:
            self.extend_html = markdown.markdown(
                self.extend,
                output_format='html',
                extensions=MD_EXTENSIONS
            )
        super(Entry, self).save(force_insert, force_update)
