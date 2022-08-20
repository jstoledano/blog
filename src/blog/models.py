import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
import markdown
from django.urls import reverse

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    def save(self, force_insert=False, force_update=False, **kwargs) -> None:
        self.description_html = markdown.markdown(
            self.description,
            output_format='html',
            extensions=MD_EXTENSIONS
        )

    def __str__(self) -> str:
        return self.name

    def permalink(self) -> str:
        return f'/category/{self.slug}'

    def get_absolute_url(self) -> str:
        return reverse('blog:category_detail', args=[self.slug])
