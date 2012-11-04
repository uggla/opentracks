# Create your views here.

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Activity
from datetime import datetime, date, time, tzinfo, timedelta

def lastweek_activity(request):
    
    lastweek = Activity.objects.filter(public = True).filter(datetime__gt = datetime.now()-timedelta(days=7))
    return render(request, 'ot_logbook/lastweek_activity.html', {'lastweek': lastweek})
