# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
import warnings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, SiteProfileNotAvailable,
)



class FernandUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        #assert False, "in user manager"
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        #email = UserManager.normalize_email(email)
        user = FernandUser(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

LANGUAGE_CHOICES = (
                    ('en', 'EN'),
                    ('nl', 'NL'),
                    ('fr', 'FR')
                    )

class FernandUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    alternate_email = models.EmailField(_('email address - alternate'), blank=True)
    structure_name = models.CharField(_('company name'), max_length=100, blank=True)
    job_title = models.CharField(_('job title'), max_length=100, blank=True)
    email_invalid = models.BooleanField(_('email invalid'), default=False)
    address = models.CharField(_('address'), max_length=250, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=30, blank=True)
    city = models.CharField(_('city'), max_length=30, blank=True)
    state_or_province = models.CharField(_('state or province'), max_length=30, blank=True)
    country_id = models.CharField(_('country code (ex: BE)'), max_length=30, blank=True)
    phone = models.CharField(_('phone number'), max_length=30, blank=True)
    phone_mobile = models.CharField(_('phone number - mobile'), max_length=30, blank=True)
    phone_alternate = models.CharField(_('phone number - alternate'), max_length=30, blank=True)
    fax = models.CharField(_('fax number'), max_length=30, blank=True)
    language_id = models.CharField(_('language EN / FR / NL'), max_length=2, choices=LANGUAGE_CHOICES)
    gender = models.CharField(_('gender'), max_length=30, blank=True)
    birthday = models.CharField(_('birthday'), max_length=30, blank=True)
    place_of_birth = models.CharField(_('place of birth'), max_length=30, blank=True)
    website = models.CharField(_('website'), max_length=50, blank=True)
    national_number = models.CharField(_('national number'), max_length=30, blank=True)
    id_card_number = models.CharField(_('id card number'), max_length=30, blank=True)
    sis_number = models.CharField(_('sis number'), max_length=30, blank=True)
    vat = models.CharField(_('vat number'), max_length=30, blank=True)
    rc = models.CharField(_('company registration number'), max_length=30, blank=True)
    
    subscribed_to_mailing = models.BooleanField(_('subscribed to mailing'), default=True)
    
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = FernandUserManager()

    USERNAME_FIELD = 'email'
    
    """
    There’s all this stuff on the current site, lets see what we need, or need not define:
    # ID
    Activity
    IsLocked
    # CreatorID
    # OwnerID
    GroupID
    # ModifierID
    ContactType
    # Password
    Denomination
    # FirstName
    # LastName
    # ClientCode
    # Email1
    EmailInvalid
    Title
    Address
    PostalCode
    City
    StateOrProvince
    CountryID
    Phone2
    MobilePhone
    Fax
    LanguageID
    Phone1
    Email2
    WebSite
    Gender
    BirthDay
    PlaceOfBirth
    NationalNumber
    IDCardNumber
    SISNumber
    DigitalInfo1
    DigitalInfo2
    Vat
    RC
    Bank1
    Bank1IBAN
    Bank1Info
    Bank2
    Bank2IBAN
    Bank2Info
    Notes
    AdminNotes
    # CreationDate
    # ModificationDate
    Privacy1
    Privacy2
    Purpose
    BillingRate
    Prefs
    Preview
    # SearchText 
    """

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        #abstract = True,cc

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if not self.first_name and not self.last_name:
            return self.email
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn(
            "The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
            PendingDeprecationWarning)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                    self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.get_full_name()

class Category(models.Model):
    title = models.CharField(_("Title (EN)"), max_length=255)
    title_nl = models.CharField(_("Title (NL)"), max_length=255)
    title_fr = models.CharField(_("Title (FR)"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, help_text=_("Unique identifier to be used in a web address: uses only unaccented letters, - and _"))
    
    members = models.ManyToManyField(FernandUser, blank=True)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.title

class PasswordReset(models.Model):
    user = models.ForeignKey(FernandUser)
    key = models.CharField(max_length=100)
    used = models.BooleanField(default=False)
