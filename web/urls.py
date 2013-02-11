# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.conf import settings
import django.contrib.admin

django.contrib.admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(django.contrib.admin.site.urls)),
    url(r'^$', 'app.views.index'),
    url(r'^fuck/$', 'app.views.fuck'),
    url(r'^fuckit/(?P<uid>[0-9]+)/$', 'app.views.fuckit'),
    url(r'', include('social_auth.urls')),
)

if settings.DEBUG or True:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
