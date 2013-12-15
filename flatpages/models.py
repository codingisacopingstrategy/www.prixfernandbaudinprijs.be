from django.db import models
from django.utils.translation import ugettext_lazy as _

class FlatPage(models.Model):
    title = models.CharField(_("Title (EN)"), max_length=255)
    title_nl = models.CharField(_("Title (NL)"), max_length=255)
    title_fr = models.CharField(_("Title (FR)"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier to be used in a web address: uses only unaccented letters, - and _"))
    content = models.TextField(_("Content (EN)"))
    content_nl = models.TextField(_("Content (NL)"), blank=True)
    content_fr = models.TextField(_("Content (FR)"), blank=True)

    def __unicode__(self):
        return self.title
    @models.permalink
    def get_absolute_url(self):
        return ('flatpage-detail', (), {'slug': str(self.slug)})
