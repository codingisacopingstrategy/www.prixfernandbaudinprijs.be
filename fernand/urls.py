from django.conf.urls import patterns, include, url

from django.conf.urls.i18n import i18n_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fernand.views.home', name='home'),
    # url(r'^fernand/', include('fernand.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += i18n_patterns('',
    url(r'^$', 'flatpages.views.flatpage', name='home'),
    url(r'^(?P<slug>[\w-]+)$', 'flatpages.views.flatpage', name='flatpage-detail'),
)
