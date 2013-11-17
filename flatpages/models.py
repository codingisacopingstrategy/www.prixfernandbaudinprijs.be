from django.db import models
from django.utils.translation import ugettext_lazy as _

class FlatPage(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title (EN)"))
    title_nl = models.CharField(max_length=255, verbose_name=_("Title (NL)"))
    title_fr = models.CharField(max_length=255, verbose_name=_("Title (FR)"))
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier. Allows a constant targeting of this page."))
    content = models.TextField(_("Content (EN)"))
    content_nl = models.TextField(_("Content (NL)"), blank=True)
    content_fr = models.TextField(_("Content (FR)"), blank=True)

    def __unicode__(self):
        return self.title
    @models.permalink
    def get_absolute_url(self):
        return ('flatpage-detail', (), {'slug': str(self.slug)})
