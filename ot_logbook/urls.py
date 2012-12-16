from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Activity, EquipmentForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',direct_to_template, {'template': 'ot_logbook/index.html'},name='main'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'ot_logbook/login.html'},name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/ot_logbook'},name='logout'),
    url(r'^activity/$','ot_logbook.views.last_week_activity' ,name='activity'),
    url(r'^activity/lastweek/$','ot_logbook.views.last_week_activity',name='last_week_activity'),
    url(r'^activity/public_activities/$','ot_logbook.views.public_activities',name='public_activities'),
    url(r'^activity/show_today/$','ot_logbook.views.show_today_activity',name='show_today_activity'),
    url(r'^activity/show_date/(?P<date>\d\d\d\d-\d\d-\d\d)/(?P<act>\d+|latest)/$','ot_logbook.views.show_date_activity',name='show_date_activity'),
    url(r'^activity/(?P<pk>\d+)/$',
       DetailView.as_view(
           model=Activity,
           context_object_name='activity',
           template_name='ot_logbook/activity_detail.html'),name='show_activity'),
    url(r'^equipment/new/$','ot_logbook.views.new_equipment',name='new_equipment'),
)
