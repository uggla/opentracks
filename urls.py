from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^s_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'opentracks.views.home', name='home'),
    # url(r'^opentracks/', include('opentracks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$',include('ot_logbook.urls')),
    (r'^$', lambda x: HttpResponseRedirect(reverse('main'))),
    url(r'^ot_logbook/',include('ot_logbook.urls'),name='main'),
)
