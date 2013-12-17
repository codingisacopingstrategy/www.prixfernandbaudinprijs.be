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
    # towards nothing (^$): home
    # foldername.filename.functionname
    
    # books
    url(r'^register$', 'books.views.register', name='register'),
    url(r'^(?P<slug>[\w-]+)/edit$', 'books.views.edit', name='books-edit'),
    url(r'^(?P<slug>[\w-]+)/collaborators/$', 'books.views.edit_book_collaborators', name='books-edit-collaborators'),
    url(r'^(?P<slug>[\w-]+)/collaborators/add$', 'books.views.add_book_collaborator', name='books-add-collaborators'),
    url(r'^(?P<slug>[\w-]+)/submit$', 'books.views.submit', name='books-submit'),
    # people
    url(r'^$', 'books.views.register_login', name='login'),
    url(r'^signup$', 'books.views.register_signup', name='signup'),
    url(r'^logout$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^(?P<slug>[\w-]+)$', 'flatpages.views.flatpage', name='flatpage-detail'),
)
