# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
    
class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("The title of the category"))
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier. Allows a constant targeting of this page."))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title
# we put the Category model before the Book model because it is called in Book and thus must be defined before.
class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    subtitle = models.CharField(max_length=255, verbose_name=_("Subtitle (if any)"), blank=True)
    publication_year = models.IntegerField(verbose_name=_("Publication year"))
    legal_depot = models.IntegerField(verbose_name=_("Legal Depot"), blank=True)
    isbn = models.IntegerField(verbose_name=_("ISBN"))
    category = models.ForeignKey(Category)
    concept = models.TextField(verbose_name=_("Editorial concept"))
    comments = models.TextField(verbose_name=_("Comments"))
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier. Allows a constant targeting of this page."))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title
    
class Technical_sheet(models.Model):
    # bookbinder = models.ForeignKey()
    printrun = models.IntegerField(verbose_name=_("Print run"), blank=True)
    dimensions = models.CharField(max_length=255, verbose_name=_("Dimensions of the book when it is closed"), blank=True)
    weight = models.IntegerField(verbose_name=_("Weight of the book"), blank=True)
    pages_number = models.IntegerField(verbose_name=_("Pages number"), blank=True)
    sections = models.IntegerField(verbose_name=_("Number of sections"), blank=True)
    paper = models.CharField(max_length=255, verbose_name=_("Paper"), blank=True)
    binding = models.CharField(max_length=255, verbose_name=_("Type of binding"), blank=True)
    printing_type = models.CharField(max_length=255, verbose_name=_("Type of printing"), blank=True)
    fonts = models.CharField(max_length=255, verbose_name=_("Fonts"), blank=True)
    cover_pages = models.CharField(max_length=255, verbose_name=_("Cover’s number of pages"), blank=True)
    cover_paper = models.CharField(max_length=255, verbose_name=_("Cover’s paper"), blank=True)
    cover_printing_type = models.CharField(max_length=255, verbose_name=_("Cover’s type of printing"), blank=True)
    cover_finish = models.CharField(max_length=255, verbose_name=_("Cover’s finish"), blank=True)
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier. Allows a constant targeting of this page."))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title
    
class Technical_sheet(models.Model):
    # collaborator = models.ForeignKey()
    # type_of_collaboration = models.ForeignKey()
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier. Allows a constant targeting of this page."))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title