from django.conf.urls import patterns, include, url

from django.conf.urls.i18n import i18n_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^export-email$', 'people.views.email_export', name='people-export-email'),
    url(r'^export-email/details$', 'people.views.email_export_detail', name='people-export-email'),
)


