# -*- coding: utf-8 -*-

import datetime
import re

from django.db import models, IntegrityError
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
    people = models.ManyToManyField(FernandUser, through='Collaboration', help_text=_("<br />You need to register at least one editor, one graphic designer, one printer, one binder, even if they are the same persons."))
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier to be used in a web address: uses only unaccented letters, - and _"))
    
    def save(self, *args, **kwargs):
    # http://www.copyandwaste.com/posts/view/unique-slugs-for-django-objects/
    
        #set pub_date as right now
        self.pub_date=datetime.datetime.now()
        #As long as this object does NOT have a slug
        if not self.slug:
           from django.template.defaultfilters import slugify

           #Take the title and replace spaces with hypens, make lowercase
           potential_slug = slugify(self.title)
           self.slug = potential_slug

           while True:
              try:
                  #try to save the object
                 super(Book, self).save(*args, **kwargs)
      
              #if this slug already exists we get an error
              except IntegrityError:
                #match the slug or look for a trailing number
                 match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
     
                 #if we find a match
                 if match_obj:
                     #take the found number and increment it by 1
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + "-" + str(next_int)
                 else:
                     #There are no matches for -# so create one with -2
                    self.slug += '-2'
                    #different error than IntegrityError
              else:
                 break
    
    def __unicode__(self):  # Python 3: def __str__(self):
            return self.title
    
class Technical_sheet(models.Model):
    printrun = models.IntegerField(_("Print run"), blank=True)
    dimensions = models.CharField(_("Dimensions of the book when it is closed"), max_length=255, blank=True)
    weight = models.IntegerField(_("Weight of the book"), blank=True)
    pages_number = models.IntegerField(_("Pages number"), blank=True)
    sections = models.IntegerField(_("Number of sections"), blank=True)
    paper = models.CharField(_("Paper(s)"), max_length=255, blank=True)
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
