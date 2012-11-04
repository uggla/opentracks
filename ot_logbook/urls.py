from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template
#from courses.models import Article

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',direct_to_template, {'template': 'ot_logbook/index.html'},name='main'),
    url(r'^lastweek/$','ot_logbook.views.lastweek_activity',name='lastweek_activity')

)
