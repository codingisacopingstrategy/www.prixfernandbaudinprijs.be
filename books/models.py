# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from people.models import FernandUser
# Create your models here.
    
class Category(models.Model):
    title = models.CharField(_("Title (EN)"), max_length=255)
    title_nl = models.CharField(_("Title (NL)"), max_length=255)
    title_fr = models.CharField(_("Title (FR)"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier to be used in a web address: uses only unaccented letters, - and _"))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title
# we put the Category model before the Book model because it is called in Book and thus must be defined before.

class Book(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    subtitle = models.CharField(_("Subtitle (if any)"), max_length=255, blank=True)
    publication_year = models.IntegerField(_("Publication year"))
    legal_depot = models.CharField(_("Legal Depot"), max_length=255, blank=True)
    isbn = models.CharField(_("ISBN"), max_length=20)
    category = models.ForeignKey(Category)
    concept = models.TextField(_("Editorial concept"))
    comments = models.TextField(_("Comments"), blank=True)
    people = models.ManyToManyField(FernandUser, through='Collaboration')
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier to be used in a web address: uses only unaccented letters, - and _"))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title
    
class Technical_sheet(models.Model):
    printrun = models.IntegerField(_("Print run"), blank=True)
    dimensions = models.CharField(_("Dimensions of the book when it is closed"), max_length=255, blank=True)
    weight = models.IntegerField(_("Weight of the book"), blank=True)
    pages_number = models.IntegerField(_("Pages number"), blank=True)
    sections = models.IntegerField(_("Number of sections"), blank=True)
    paper = models.CharField(_("Paper"), max_length=255, blank=True)
    binding = models.CharField(_("Type of binding"), max_length=255, blank=True)
    printing_type = models.CharField(_("Type of printing"), max_length=255, blank=True)
    fonts = models.CharField(_("Fonts"), max_length=255, blank=True)
    cover_pages = models.CharField(_("Cover’s number of pages"), max_length=255, blank=True)
    cover_paper = models.CharField(_("Cover’s paper"), max_length=255, blank=True)
    cover_printing_type = models.CharField(_("Cover’s type of printing"), max_length=255, blank=True)
    cover_finish = models.CharField(_("Cover’s finish"), max_length=255, blank=True)
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier to be used in a web address: uses only unaccented letters, - and _"))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

class Role(models.Model):
    title = models.CharField(_("Title (EN)"), max_length=255)
    title_nl = models.CharField(_("Title (NL)"), max_length=255)
    title_fr = models.CharField(_("Title (FR)"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier to be used in a web address: uses only unaccented letters, - and _"))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

class Collaboration(models.Model):
    book = models.ForeignKey(Book)
    person = models.ForeignKey(FernandUser)
    role = models.ForeignKey(Role)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s is %s for %s" % (self.person, self.role, self.book)
